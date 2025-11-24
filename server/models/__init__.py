from .deepfake_detection import DeepfakeDetectorModel, CNNDeepfakeDetector
from .deepfake_generation import DeepfakeGeneratorModel, SimpleFaceSwapGenerator

__all__ = [
    'DeepfakeDetectorModel',
    'CNNDeepfakeDetector',
    'DeepfakeGeneratorModel',
    'SimpleFaceSwapGenerator'
]
