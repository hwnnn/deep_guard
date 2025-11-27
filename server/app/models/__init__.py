from .base import DeepfakeDetectorModel
from .cnn_detector import CNNDeepfakeDetector
from .deepface_detector import DeepFaceDetector
from .face_recognition_detector import FaceRecognitionDetector
from .ensemble_detector import EnsembleDetector
from .insightface_detector import InsightFaceDetector

__all__ = [
    "DeepfakeDetectorModel",
    "CNNDeepfakeDetector",
    "DeepFaceDetector",
    "FaceRecognitionDetector",
    "EnsembleDetector",
    "InsightFaceDetector"
]
