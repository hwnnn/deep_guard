from models.deepfake_generation import SimpleFaceSwapGenerator


class DeepfakeGenerationService:
    
    def __init__(self):
        self.generator = SimpleFaceSwapGenerator()
    
    async def generate_deepfake(self, source_bytes: bytes, target_bytes: bytes) -> bytes:
        """
        딥페이크 생성
        
        Args:
            source_bytes: 소스 얼굴 이미지
            target_bytes: 타겟 이미지
            
        Returns:
            생성된 딥페이크 이미지 bytes
        """
        return self.generator.generate(source_bytes, target_bytes)
    
    def get_generator_info(self) -> dict:
        return {
            "name": self.generator.name,
            "type": "Face Swap Generator"
        }
