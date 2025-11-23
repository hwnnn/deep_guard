from abc import ABC, abstractmethod


class DeepfakeGeneratorModel(ABC):
    
    @abstractmethod
    def generate(self, source: bytes, target: bytes) -> bytes:
        """
        딥페이크 이미지 생성
        
        Args:
            source: 소스 얼굴 이미지
            target: 타겟 이미지 (얼굴이 교체될 이미지)
            
        Returns:
            생성된 딥페이크 이미지 bytes
        """
        raise NotImplementedError
