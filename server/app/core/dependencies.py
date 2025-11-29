from app.core.config import get_settings
from app.db.database import db, DatabaseManager
from app.models import EnsembleDetector
from functools import lru_cache
from app.models.DeepfakeBench_main.deepfake_detector import DeepfakeDetector

WEIGHTS_PATH = "app/models/DeepfakeBench_main/training/pretrained/xception_best.pth"
#deepfake_detector = EnsembleDetector()

@lru_cache()
def get_deepfake_detector():
    deepfake_detector = DeepfakeDetector(weights_path = WEIGHTS_PATH, device='cpu')
    return deepfake_detector

def get_app_settings():
    return get_settings()


def get_db() -> DatabaseManager:
    """데이터베이스 매니저 의존성"""
    return db