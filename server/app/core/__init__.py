"""
Core module for configuration and dependencies
"""
from .config import Settings, get_settings
from .dependencies import get_deepfake_detector, get_app_settings, get_db

__all__ = [
    "Settings",
    "get_settings",
    "get_deepfake_detector",
    "get_app_settings",
    "get_db",
]
