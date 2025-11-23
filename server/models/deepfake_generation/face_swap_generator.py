from io import BytesIO
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import cv2
from .base import DeepfakeGeneratorModel


class SimpleFaceSwapGenerator(DeepfakeGeneratorModel):
    """
    간단한 얼굴 교체 생성기
    실제 DeepFaceLab이나 Faceswap은 복잡한 GAN 모델을 사용하지만,
    여기서는 안전한 방식으로 기본적인 얼굴 교체 구현
    """
    
    def __init__(self):
        self.name = "simple_face_swap_v1"
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def generate(self, source: bytes, target: bytes) -> bytes:
        """얼굴 교체 생성"""
        # 이미지 로드
        source_img = Image.open(BytesIO(source)).convert("RGB")
        target_img = Image.open(BytesIO(target)).convert("RGB")
        
        source_cv = cv2.cvtColor(np.array(source_img), cv2.COLOR_RGB2BGR)
        target_cv = cv2.cvtColor(np.array(target_img), cv2.COLOR_RGB2BGR)
        
        # 얼굴 검출
        source_faces = self._detect_faces(source_cv)
        target_faces = self._detect_faces(target_cv)
        
        if len(source_faces) == 0:
            raise ValueError("Source image does not contain any faces")
        if len(target_faces) == 0:
            raise ValueError("Target image does not contain any faces")
        
        # 첫 번째 얼굴 사용
        source_face = source_faces[0]
        target_face = target_faces[0]
        
        # 얼굴 교체 수행
        result = self._swap_faces(source_cv, target_cv, source_face, target_face)
        
        # PIL Image로 변환 후 반환
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result_img = Image.fromarray(result_rgb)
        
        # 품질 저하 효과 추가 (딥페이크 특성)
        result_img = self._add_compression_artifacts(result_img)
        
        # JPEG로 저장
        output = BytesIO()
        result_img.save(output, format='JPEG', quality=90)
        return output.getvalue()
    
    def _detect_faces(self, img: np.ndarray) -> list:
        """얼굴 검출"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces
    
    def _swap_faces(
        self, 
        source_img: np.ndarray, 
        target_img: np.ndarray,
        source_face: tuple,
        target_face: tuple
    ) -> np.ndarray:
        """얼굴 교체"""
        sx, sy, sw, sh = source_face
        tx, ty, tw, th = target_face
        
        # 소스 얼굴 추출 및 리사이징
        source_face_region = source_img[sy:sy+sh, sx:sx+sw]
        source_face_resized = cv2.resize(source_face_region, (tw, th))
        
        # 결과 이미지 생성
        result = target_img.copy()
        
        # 마스크 생성 (타원형)
        mask = np.zeros((th, tw), dtype=np.uint8)
        center = (tw // 2, th // 2)
        axes = (tw // 2 - 5, th // 2 - 5)
        cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)
        
        # 마스크 블러링 (자연스러운 경계)
        mask = cv2.GaussianBlur(mask, (15, 15), 0)
        
        # 피부 톤 조정
        source_face_adjusted = self._adjust_skin_tone(
            source_face_resized, 
            target_img[ty:ty+th, tx:tx+tw]
        )
        
        # 알파 블렌딩
        mask_3d = np.dstack([mask] * 3) / 255.0
        target_region = result[ty:ty+th, tx:tx+tw]
        blended = (source_face_adjusted * mask_3d + 
                  target_region * (1 - mask_3d)).astype(np.uint8)
        
        result[ty:ty+th, tx:tx+tw] = blended
        
        # 경계 블렌딩
        result = self._seamless_clone(result, tx, ty, tw, th)
        
        return result
    
    def _adjust_skin_tone(self, source: np.ndarray, target: np.ndarray) -> np.ndarray:
        """피부 톤 조정"""
        source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
        target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB)
        
        # L, A, B 채널별 평균 계산
        source_mean = source_lab.mean(axis=(0, 1))
        target_mean = target_lab.mean(axis=(0, 1))
        
        # 채널별 보정
        adjusted_lab = source_lab.copy().astype(np.float32)
        for i in range(3):
            adjusted_lab[:, :, i] += (target_mean[i] - source_mean[i]) * 0.3
        
        adjusted_lab = np.clip(adjusted_lab, 0, 255).astype(np.uint8)
        return cv2.cvtColor(adjusted_lab, cv2.COLOR_LAB2BGR)
    
    def _seamless_clone(
        self, 
        img: np.ndarray, 
        x: int, 
        y: int, 
        w: int, 
        h: int
    ) -> np.ndarray:
        """Seamless cloning으로 자연스러운 경계 생성"""
        try:
            # 마스크 생성
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            center = (x + w // 2, y + h // 2)
            cv2.ellipse(
                mask, 
                center, 
                (w // 2 - 10, h // 2 - 10), 
                0, 0, 360, 255, -1
            )
            
            # Seamless clone
            result = cv2.seamlessClone(
                img, img, mask, center, cv2.NORMAL_CLONE
            )
            return result
        except:
            return img
    
    def _add_compression_artifacts(self, img: Image.Image) -> Image.Image:
        """압축 아티팩트 추가 (딥페이크 특성)"""
        # 약간의 블러
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # 샤프니스 감소
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(0.95)
        
        return img
