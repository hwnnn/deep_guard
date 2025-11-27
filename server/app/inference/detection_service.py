from app.models import CNNDeepfakeDetector
from typing import Dict, Any


class DeepfakeDetectionService:
    
    def __init__(self):
        self.detector = CNNDeepfakeDetector()
    
    async def detect_deepfake(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        이미지가 딥페이크인지 탐지
        
        Returns:
            탐지 결과 딕셔너리
        """
        return self.detector.detect(image_bytes)
    
    def get_detector_info(self) -> Dict[str, str]:
        return {
            "name": self.detector.name,
            "type": "CNN-based Deepfake Detector"
        }
