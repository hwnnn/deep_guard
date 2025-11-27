from app.core.config import get_settings
from app.db.database import db, DatabaseManager
from app.models import EnsembleDetector

deepfake_detector = EnsembleDetector()

def get_deepfake_detector():
    return deepfake_detector

def get_app_settings():
    return get_settings()


def get_db() -> DatabaseManager:
    """데이터베이스 매니저 의존성"""
    return db