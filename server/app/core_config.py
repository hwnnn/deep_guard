from functools import lru_cache

import os

class Settings:
    """Lightweight settings replacement (pydantic-free fallback).
    실제 서비스 단계에서 pydantic-settings 로 교체 가능."""

    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME", "deep_guard_backend")
        self.API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api")
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
        origins = os.getenv("BACKEND_CORS_ORIGINS", "*")
        self.BACKEND_CORS_ORIGINS = [o.strip() for o in origins.split(",") if o.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
