from .core_config import get_settings
from models.deepfake_detection import EnsembleDetector

deepfake_detector = EnsembleDetector()

def get_deepfake_detector():
    return deepfake_detector

def get_app_settings():
    return get_settings()