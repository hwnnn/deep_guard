# DeepfakeBench Xception model is now used for inference
# Previous detection models (CNN, DeepFace, etc.) have been removed

from .DeepfakeBench_main.deepfake_detector import DeepfakeDetector

__all__ = [
    "DeepfakeDetector"
]
