from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .routers import server
from .core_config import get_settings
import time
from fastapi import Request

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="1.0.0",
    description="Deep Guard - Face Swap & Deepfake Detection API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "version": "1.0.0"}


app.include_router(server.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {
        "message": "deep_guard backend running",
        "version": "1.0.0",
        "api_prefix": settings.API_V1_PREFIX
    }
