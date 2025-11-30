import sys
import os
from pathlib import Path
import torch
import cv2
import dlib
import numpy as np
from PIL import Image
from torchvision import transforms

current_file_path = Path(__file__).resolve()
deepfake_bench_root = current_file_path.parent

if str(deepfake_bench_root) not in sys.path:
    sys.path.append(str(deepfake_bench_root))

if not torch.cuda.is_available():
    torch.cuda.get_device_name = lambda *args, **kwargs: ""

try:
    from training.detectors.xception_detector import XceptionDetector
except ImportError:
    sys.path.append(str(deepfake_bench_root))
    from training.detectors.xception_detector import XceptionDetector

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget


class DeepfakeBenchWrapper(torch.nn.Module):
    def __init__(self, model):
        super(DeepfakeBenchWrapper, self).__init__()
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
        
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize([0.5]*3, [0.5]*3)
        ])

    def _load_model(self):
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
            kwargs['map_location'] = torch.device('cpu')
            return original_torch_load(*args, **kwargs)
            
        try:
            torch.load = safe_cpu_load
            model = XceptionDetector(config)
        finally:
            torch.load = original_torch_load

        try:
            checkpoint = torch.load(self.weights_path, map_location=self.device)
            state_dict = checkpoint.get('state_dict') or checkpoint.get('model') or checkpoint
            
            new_state_dict = {}
            for k, v in state_dict.items():
                name = k.replace("module.", "") 
                new_state_dict[name] = v
            
            model.load_state_dict(new_state_dict, strict=False)
            model.eval().to(self.device)
            
            return model
        except Exception as e:
            raise RuntimeError(f"가중치 적용 실패: {e}")

    def detect(self, image_input):
        pil_img = self._get_cropped_face(image_input)
        if pil_img is None:
            return None, None, None, None

        img_tensor = self.transform(pil_img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            input_data = {'image': img_tensor, 'label': torch.tensor([0]).to(self.device)}
            prob = self.model(input_data, inference=True)['prob'].item()

        is_fake = prob > 0.5

        target_category = 1 if is_fake else 0
        target_layers = [self.model.backbone.conv4] 

        cam = GradCAM(model=self.cam_wrapper, target_layers=target_layers)
        targets = [ClassifierOutputTarget(target_category)]
        
        grayscale_cam = cam(input_tensor=img_tensor, targets=targets)[0, :]

        pil_img_resized = pil_img.resize((256, 256))
        cropped_img_np = np.array(pil_img_resized)
        
        rgb_img_float = cropped_img_np.astype(np.float32) / 255.0
        
        vis_image = self._apply_cam_on_image(rgb_img_float, grayscale_cam, threshold=0.3)

        return is_fake, prob, vis_image, cropped_img_np

    def _get_cropped_face(self, image_input):
        if isinstance(image_input, str):
            img = cv2.imread(image_input)
        else:
            img = cv2.imdecode(np.frombuffer(image_input, np.uint8), cv2.IMREAD_COLOR)
        
        if img is None: return None

        detector = self.face_detector
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        if not faces: return None

        face = faces[0]
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        
        w, h = x2 - x1, y2 - y1
        margin = int(w * 0.2)
        x1, y1 = max(0, x1 - margin), max(0, y1 - margin)
        x2, y2 = min(img.shape[1], x2 + margin), min(img.shape[0], y2 + margin)

        cropped_img_bgr = img[y1:y2, x1:x2]
        return Image.fromarray(cv2.cvtColor(cropped_img_bgr, cv2.COLOR_BGR2RGB))

    def _apply_cam_on_image(self, img, mask, threshold=0.3, image_weight=0.5):
        """
        빨간색 + 투명도로 GradCAM 시각화
        mask 값이 높을수록 불투명한 빨간색, 낮을수록 투명
        """
        # ===== 이전 코드 (JET 컬러맵 사용) =====
        # mask_filtered = np.where(mask > threshold, mask, 0)
        # heatmap = cv2.applyColorMap(np.uint8(255 * mask_filtered), cv2.COLORMAP_JET)
        # heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        # heatmap = np.float32(heatmap) / 255
        # if np.max(img) > 1:
        #     raise Exception("The input image should np.float32 in the range [0, 1]")
        # if image_weight < 0 or image_weight > 1:
        #     raise Exception(f"image_weight should be in the range [0, 1]. Got: {image_weight}")
        # binary_mask = mask > threshold
        # binary_mask_3d = np.stack([binary_mask, binary_mask, binary_mask], axis=-1)
        # cam = np.where(
        #     binary_mask_3d,
        #     (1 - image_weight) * heatmap + image_weight * img,
        #     img
        # )
        # cam = cam / np.max(cam)
        # return np.uint8(255 * cam)
        
        # ===== 새로운 코드 (빨간색 + 투명도) =====
        if np.max(img) > 1:
            raise Exception("The input image should np.float32 in the range [0, 1]")

        # 원본 이미지를 uint8로 변환
        img_uint8 = np.uint8(255 * img)
        
        # 빨간색 오버레이 생성 (RGB: 255, 0, 0)
        red_overlay = np.zeros_like(img_uint8)
        red_overlay[:, :, 0] = 255  # R 채널만 255
        
        # mask를 투명도(alpha)로 사용 (0~1 범위)
        # threshold 이하는 완전 투명, 이상은 mask 값에 비례한 투명도
        alpha = np.where(mask > threshold, mask, 0)
        alpha = np.clip(alpha, 0, 1)  # 0~1 범위로 클리핑
        alpha = alpha * 0.5  # 투명도를 50%로 조정
        alpha_3d = np.stack([alpha, alpha, alpha], axis=-1)
        
        # 빨간색 오버레이를 원본 이미지에 블렌딩
        # alpha가 높을수록 빨간색이 진하게 표시됨
        blended = (1 - alpha_3d) * img_uint8 + alpha_3d * red_overlay
        
        return np.uint8(blended)