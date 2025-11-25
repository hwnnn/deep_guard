from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import numpy as np


class DeepfakeDetectorModel(ABC):
    
    @abstractmethod
    def detect(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        이미지가 딥페이크인지 탐지
        
        Returns:
            {
                "is_fake": bool,
                "confidence": float,  # 0.0 ~ 1.0
                "fake_probability": float,
                "real_probability": float,
                "suspicious_regions": list  # 의심스러운 영역 좌표
            }
        """
        raise NotImplementedError
