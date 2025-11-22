from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import server
from .core_config import get_settings

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple healthcheck
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}

# Unified inference router for web and mobile clients
app.include_router(server.router, prefix=settings.API_V1_PREFIX)

# Optional root
@app.get("/")
async def root():
    return {"message": "deep_guard backend running"}
