from app.models import DeepfakeDetector
from typing import Dict, Any


class DeepfakeDetectionService:
    
    def __init__(self):
        WEIGHTS_PATH = "app/models/DeepfakeBench_main/training/pretrained/xception_best.pth"
        self.detector = DeepfakeDetector(weights_path=WEIGHTS_PATH, device='cpu')
    
    async def detect_deepfake(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        이미지가 딥페이크인지 탐지
        
        Returns:
            탐지 결과 딕셔너리
        """
        result = self.detector.detect(image_bytes)
        
        if result[0] is None:
            return {
                "error": "No face detected in image",
                "is_fake": None,
                "confidence": None
            }
        
        is_fake, prob, vis_image, cropped_img = result
        fake_prob = float(prob) if prob is not None else 0.0
        
        return {
            "is_fake": bool(is_fake),
            "fake_probability": fake_prob,
            "real_probability": 1.0 - fake_prob,
            "confidence": max(fake_prob, 1.0 - fake_prob),
            "verdict": "🚨 DEEPFAKE DETECTED" if is_fake else "✓ AUTHENTIC IMAGE",
            "visualization": vis_image.tolist() if vis_image is not None else None,
            "cropped_face": cropped_img.tolist() if cropped_img is not None else None
        }
    
    def get_detector_info(self) -> Dict[str, str]:
        return {
            "name": "Xception",
            "type": "DeepfakeBench Xception Detector"
        }
