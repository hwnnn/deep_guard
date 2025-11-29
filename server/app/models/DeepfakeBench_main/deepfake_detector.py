import sys
import os
from pathlib import Path

current_file_path = Path(__file__).resolve()
deepfake_bench_root = current_file_path.parent

if str(deepfake_bench_root) not in sys.path:
    sys.path.append(str(deepfake_bench_root))

import torch
import cv2
import dlib
import numpy as np
from PIL import Image
from torchvision import transforms
if not torch.cuda.is_available():
    torch.cuda.get_device_name = lambda *args, **kwargs: ""

try:
    from training.detectors.xception_detector import XceptionDetector
except ImportError:
    sys.path.append(str(deepfake_bench_root))
    from training.detectors.xception_detector import XceptionDetector

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget

# Grad-CAM용 Wrapper
class DeepfakeBenchWrapper(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model
    def forward(self, x):
        input_data = {'image': x, 'label': torch.tensor([0]).to(x.device)}
        return self.model(input_data, inference=True)['cls']

class DeepfakeDetector:
    def __init__(self, weights_path, device='cpu'):
        self.device = device
        self.weights_path = weights_path
        self.model = self._load_model()
        self.cam_wrapper = DeepfakeBenchWrapper(self.model)
        self.face_detector = dlib.get_frontal_face_detector()
        
        # 전처리
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize([0.5]*3, [0.5]*3)
        ])

    def _load_model(self):
        # XceptionDetector 설정값
        config = {
            'pretrained': self.weights_path,
            'backbone_name': 'xception',
            'backbone_config': {
                'mode': 'original', 
                'num_classes': 2, 
                'inc': 3, 
                'dropout': False
            },
            'loss_func': 'cross_entropy', 
        }
        

        original_torch_load = torch.load
        
        def safe_cpu_load(*args, **kwargs):
            # 무조건 CPU로 로드하도록 강제 설정
            kwargs['map_location'] = torch.device('cpu')
            return original_torch_load(*args, **kwargs)
            
        try:
            print(f"모델 초기화 중... (경로: {self.weights_path})")
            
            # 1. torch.load를 안전한 함수로 바꿔치기
            torch.load = safe_cpu_load
            model = XceptionDetector(config)
            
        finally:
            # 2. 작업이 끝나면 반드시 원래 함수로 복구
            torch.load = original_torch_load

        try:
            checkpoint = torch.load(self.weights_path, map_location=self.device)
            
            if 'state_dict' in checkpoint:
                state_dict = checkpoint['state_dict']
            elif 'model' in checkpoint:
                state_dict = checkpoint['model']
            else:
                state_dict = checkpoint
            
            # 키 이름 정리 (DataParallel의 'module.' 등 제거)
            new_state_dict = {}
            for k, v in state_dict.items():
                name = k.replace("module.", "") 
                new_state_dict[name] = v
            
            # 가중치 덮어씌우기
            model.load_state_dict(new_state_dict, strict=False)
            model.eval().to(self.device)
            
            print("모델 로드 및 가중치 적용 성공!")
            return model
            
        except Exception as e:
            raise RuntimeError(f"가중치 적용 실패: {e}")

    def detect(self, image_input):
        # 1. 얼굴 로드 및 크롭
        pil_img = self._get_cropped_face(image_input)
        
        if pil_img is None:
            return None, None, None

        # 2. 전처리
        img_tensor = self.transform(pil_img).unsqueeze(0).to(self.device)
        
        # 3. 추론
        with torch.no_grad():
            input_data = {'image': img_tensor, 'label': torch.tensor([0]).to(self.device)}
            prob = self.model(input_data, inference=True)['prob'].item()

        is_fake = prob > 0.5

        # 4. Grad-CAM 생성
        target_category = 1 if is_fake else 0
        
        # DeepfakeBench Xception 구조의 마지막 Conv 레이어
        target_layers = [self.model.backbone.conv4]

        cam = GradCAM(model=self.cam_wrapper, target_layers=target_layers)
        grayscale_cam = cam(input_tensor=img_tensor, targets=[ClassifierOutputTarget(target_category)])[0, :]

        # 5. 시각화 이미지 합성
        rgb_img_resized = np.array(pil_img.resize((256, 256))).astype(np.float32) / 255.0
        vis_image = self._apply_cam_on_image(rgb_img_resized, grayscale_cam)

        return is_fake, prob, vis_image

    def _get_cropped_face(self, image_input):
        if isinstance(image_input, str):
            img = cv2.imread(image_input)
        else:
            img = cv2.imdecode(np.frombuffer(image_input, np.uint8), cv2.IMREAD_COLOR)
        
        if img is None: return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector(gray)
        if not faces: return None

        face = faces[0]
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        
        w, h = x2 - x1, y2 - y1
        margin = int(w * 0.2)
        x1, y1 = max(0, x1 - margin), max(0, y1 - margin)
        x2, y2 = min(img.shape[1], x2 + margin), min(img.shape[0], y2 + margin)

        return Image.fromarray(cv2.cvtColor(img[y1:y2, x1:x2], cv2.COLOR_BGR2RGB))

    def _apply_cam_on_image(self, img, mask):
        heatmap = cv2.applyColorMap(np.uint8(255 * mask), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        heatmap = np.float32(heatmap) / 255
        
        cam = heatmap + img
        cam = cam / np.max(cam)
        return np.uint8(255 * cam)