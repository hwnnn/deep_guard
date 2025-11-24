from functools import lru_cache
import os


class Settings:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME", "deep_guard_backend")
        self.API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api")
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
        self.MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", str(10 * 1024 * 1024)))
        origins = os.getenv("BACKEND_CORS_ORIGINS", "*")
        self.BACKEND_CORS_ORIGINS = [o.strip() for o in origins.split(",") if o.strip()]
        self.RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
        self.RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        self.RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
