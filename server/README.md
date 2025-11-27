# Deep Guard Server 🛡️

> AI-Powered Deepfake Detection API with Hybrid Storage Architecture

딥페이크 탐지를 위한 프로덕션 레벨 FastAPI 백엔드 서버입니다.  
5가지 딥페이크 탐지 모델과 Redis + MongoDB 하이브리드 스토리지를 지원합니다.

**📅 Last Updated**: 2025년 11월 25일  
**🏗️ Architecture**: Functional Module Organization (core, db, models, inference, api)

## 📋 목차

- [핵심 기능](#-핵심-기능)
- [아키텍처](#-아키텍처)
- [빠른 시작](#-빠른-시작)
- [API 사용법](#-api-사용법)
- [데이터베이스 설정](#-데이터베이스-설정)
- [환경 변수](#-환경-변수)
- [성능](#-성능)

## 🎯 핵심 기능

### 1. 딥페이크 탐지 (5가지 모델)
- **CNN Detector**: OpenCV 기반 초고속 탐지 (~50ms)
- **DeepFace Detector**: 감정/나이/성별 분석 기반 탐지 (100% 신뢰도)
- **Face Recognition Detector**: 68포인트 랜드마크 분석 (~210ms)
- **InsightFace Detector**: 512D 임베딩 벡터 분석 (~130ms)
- **Ensemble Detector** ⭐: 3가지 모델 결합으로 **89.4% 신뢰도** 달성

### 2. 하이브리드 스토리지 아키텍처
- **Redis**: 24시간 TTL 캐시 (~10ms 응답 속도)
- **MongoDB**: 영구 저장소 + 통계 집계
- **In-Memory Fallback**: DB 없이도 작동하는 안정성

### 3. 비동기 추론 API
- `POST /api/inference/upload`: 파일 업로드 → task_id 즉시 반환
- `GET /api/inference/result/{task_id}`: 추론 결과 조회 (캐시 우선)
- `GET /api/inference/statistics`: 실시간 통계 (전체/가짜/진짜 비율)

### 4. 프로덕션 레벨 기능
- 🔒 CORS 설정 및 보안 헤더
- 📊 자동 API 문서화 (Swagger UI)
- 🐳 Docker Compose 기반 배포
- ⚡ GZip 압축 미들웨어
- 📝 상세 로깅 및 디버그 모드

## 🏗️ 아키텍처

### 프로젝트 구조

```
server/
├── app/
│   ├── main.py                    # FastAPI 앱 진입점 + 라이프사이클
│   ├── core/                      # ⚙️ 설정 및 의존성
│   │   ├── config.py              # 환경 변수 관리 (Settings)
│   │   └── dependencies.py        # 의존성 주입 (get_db, get_detector)
│   ├── db/                        # 💾 데이터베이스 레이어
│   │   └── database.py            # DatabaseManager (Redis + MongoDB + Fallback)
│   ├── models/                    # 🤖 AI 탐지 모델
│   │   ├── base.py                # BaseDeepfakeDetector 추상 클래스
│   │   ├── cnn_detector.py        # CNN 기반 초고속 탐지
│   │   ├── deepface_detector.py   # 감정/나이/성별 분석 탐지
│   │   ├── face_recognition_detector.py  # 68포인트 랜드마크 탐지
│   │   ├── insightface_detector.py       # 512D 임베딩 벡터 탐지
│   │   └── ensemble_detector.py   # ⭐ 3가지 모델 앙상블 (89.4% 신뢰도)
│   ├── inference/                 # 🔬 비즈니스 로직
│   │   ├── detection_service.py   # 딥페이크 탐지 서비스
│   │   ├── api_inference.py       # API 추론 로직
│   │   └── models_comparison_inference.py  # 모델 비교 분석
│   └── api/                       # 🌐 API 엔드포인트
│       └── server.py              # 메인 라우터 (upload, result, stats)
├── dataset/                       # 📂 학습 데이터셋 (선택)
├── tests/                         # 🧪 테스트 코드
├── .env                           # 🔐 환경 변수 설정 파일
├── docker-compose.yml             # 🐳 Redis + MongoDB 컨테이너
├── requirements.txt               # 📦 Python 의존성
└── README.md
```

### 아키텍처 설계 원칙

**기능별 모듈 분리 (Functional Organization)**:
- `core/`: 애플리케이션 설정 및 의존성 관리
- `db/`: 데이터베이스 추상화 레이어
- `models/`: AI 모델 구현 (순수 추론 로직)
- `inference/`: 비즈니스 로직 및 서비스 계층
- `api/`: HTTP 엔드포인트 및 라우팅

**절대 경로 Import (app.*)**: 모든 모듈은 `app.`로 시작하는 절대 경로를 사용하여 순환 참조 방지 및 코드 가독성 향상

### 레이어 구조

```
┌──────────────────────────────────────────────┐
│          Client (Web/Mobile)                 │
└────────────────────┬─────────────────────────┘
                     │
┌────────────────────▼─────────────────────────┐
│       API Layer (app/api/server.py)          │
│  - POST /api/inference/upload                │
│  - GET  /api/inference/result/{id}           │
│  - GET  /api/inference/statistics            │
│  - GET  /health                              │
└────────────────────┬─────────────────────────┘
                     │
┌────────────────────▼─────────────────────────┐
│   Dependency Injection (app/core)            │
│  - get_deepfake_detector() → EnsembleDetector│
│  - get_db() → DatabaseManager                │
│  - get_app_settings() → Settings             │
└────────────────────┬─────────────────────────┘
                     │
      ┌──────────────┴──────────────┐
      │                             │
┌─────▼─────────────────┐    ┌─────────▼────────┐
│  Database (app/db)    │    │  Inference       │
│  - Redis (Cache)      │    │  (app/inference) │
│  - MongoDB (Store)    │    │  - detection_    │
│  - Fallback (RAM)     │    │    service       │
└─────┬─────────────────┘    │  - api_inference │
      │                      │  - comparison    │
      │                      └─────────┬────────┘
      │                                │
      │                      ┌─────────▼────────┐
      │                      │  Models (app/)   │
      │                      │  - Ensemble ⭐   │
      └──────────────────────┤  - CNN           │
                             │  - DeepFace      │
                             │  - FaceRec       │
                             │  - InsightFace   │
                             └──────────────────┘
```

### 3-Tier 스토리지 전략

1. **Redis (캐시)**: 최근 조회한 결과를 24시간 동안 메모리에 보관 (~10ms)
2. **MongoDB (DB)**: 모든 추론 결과를 영구 저장 + 통계 집계 (~50ms)
3. **In-Memory (폴백)**: Redis/MongoDB 없어도 서버 작동 보장

**데이터 흐름:**
```
Upload → Detect → Save to Redis (TTL 24h) → Save to MongoDB → Return task_id
Query  → Check Redis → Check MongoDB → Check Fallback → Return result
```

## 🚀 빠른 시작

### 요구사항

- Python 3.11+
- Docker & Docker Compose (Redis + MongoDB용)
- 4GB+ RAM (AI 모델 로딩)

### 1단계: 설치

```bash
# 1. 저장소 클론
git clone https://github.com/hwnnn/deep_guard.git
cd deep_guard/server

# 2. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. 의존성 설치
pip install -r requirements.txt
```

### 2단계: 데이터베이스 실행 (선택)

```bash
# Docker Compose로 Redis + MongoDB 실행
docker compose up -d

# 확인
docker ps  # deep_guard_redis, deep_guard_mongodb 실행 중
```

> **참고**: DB 없이도 서버는 작동합니다 (in-memory fallback)

### 3단계: 서버 실행

```bash
# 개발 모드 (자동 재시작)
python -m uvicorn app.main:app --reload --port 8000

# 프로덕션 모드
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4단계: 확인

```bash
# 루트 엔드포인트
curl http://localhost:8000/

# Health check (DB 상태 포함)
curl http://localhost:8000/health

# Swagger UI (API 문서)
open http://localhost:8000/docs
```

**출력 예시:**
```json
// GET /
{
  "message": "deep_guard backend running",
  "version": "1.0.0",
  "api_prefix": "/api"
}

// GET /health
{
  "status": "ok",
  "version": "1.0.0",
  "redis": "connected",
  "mongodb": "connected"
}
```

## 📡 API 사용법

### 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| `GET` | `/health` | 헬스체크 + DB 상태 |
| `POST` | `/api/inference/upload` | 이미지 업로드 → task_id 반환 |
| `GET` | `/api/inference/result/{task_id}` | 추론 결과 조회 (캐시 우선) |
| `GET` | `/api/inference/statistics` | 전체 통계 (total, fake, real) |

### 1. 이미지 업로드

```bash
curl -X POST "http://localhost:8000/api/inference/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/images/deepfake.jpeg"
```

**응답:**
```json
{
  "task_id": "b64a8b5d-732b-4746-a575-fca7bd9047e6",
  "status": "success",
  "message": "File uploaded and processed successfully"
}
```

### 2. 결과 조회

```bash
curl "http://localhost:8000/api/inference/result/b64a8b5d-732b-4746-a575-fca7bd9047e6"
```

**응답:**
```json
{
  "task_id": "b64a8b5d-732b-4746-a575-fca7bd9047e6",
  "filename": "deepfake.jpeg",
  "file_size": 7200,
  "timestamp": "2025-11-24T05:11:06.645516",
  "detection_result": {
    "is_fake": false,
    "confidence": 0.8932,
    "fake_probability": 0.1068,
    "real_probability": 0.8932,
    "verdict": "✓ AUTHENTIC IMAGE"
  },
  "analysis": {
    "ensemble_method": "weighted_average_70_vote_30",
    "models_used": 3,
    "fake_votes": 0,
    "model_results": {
      "CNN": {"fake_probability": 0.4188, "confidence": 0.5812},
      "DeepFace": {"fake_probability": 0.0, "confidence": 1.0},
      "FaceRecognition": {"fake_probability": 0.15, "confidence": 0.85}
    }
  },
  "model_info": {
    "name": "Ensemble (CNN + DeepFace + FaceRecognition)"
  }
}
```

### 3. 통계 조회

```bash
curl "http://localhost:8000/api/inference/statistics"
```

**응답:**
```json
{
  "total": 2,
  "fake": 0,
  "real": 2,
  "fake_rate": 0.0
}
```

### Python 클라이언트 예제

```python
import requests

# 1. 파일 업로드
with open("test_image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/inference/upload",
        files={"file": f}
    )
    task_id = response.json()["task_id"]
    print(f"Task ID: {task_id}")

# 2. 결과 조회
result = requests.get(
    f"http://localhost:8000/api/inference/result/{task_id}"
).json()

print(f"Is Fake: {result['detection_result']['is_fake']}")
print(f"Confidence: {result['detection_result']['confidence']:.2%}")
```

## 🗄️ 데이터베이스 설정

### Docker Compose로 실행 (권장)

```bash
docker compose up -d
```

**포함된 서비스:**
- `deep_guard_redis`: Redis 7 (포트 6379)
- `deep_guard_mongodb`: MongoDB 7 (포트 27017)

### 수동 설치 (macOS)

```bash
# Redis
brew install redis
brew services start redis

# MongoDB
brew install mongodb-community
brew services start mongodb-community
```

### 연결 확인

```bash
# Redis
redis-cli ping  # PONG 출력되면 정상

# MongoDB
mongosh --eval "db.version()"  # 버전 출력되면 정상
```

### 데이터 관리

```bash
# Redis 데이터 확인
docker exec deep_guard_redis redis-cli KEYS "task:*"
docker exec deep_guard_redis redis-cli TTL "task:some-task-id"

# MongoDB 데이터 확인
docker exec deep_guard_mongodb mongosh --eval \
  "db.getSiblingDB('deep_guard').inference_results.find().limit(5)"

# 전체 초기화 (주의!)
docker compose down -v
```

## ⚙️ 환경 변수

`.env` 파일을 수정하여 모든 설정을 커스터마이즈할 수 있습니다:

```env
# ============================================
# Deep Guard Server Configuration
# ============================================

# Application Settings
DEBUG=true                      # 디버그 로그 활성화
APP_NAME=Deep Guard API
APP_VERSION=1.0.0

# Redis Configuration (Cache Layer)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=                 # 비어있으면 인증 없음
REDIS_TTL=86400                 # 24시간 (초 단위)

# MongoDB Configuration (Persistent Storage)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=deep_guard
MONGODB_COLLECTION=inference_results

# API Settings
MAX_FILE_SIZE=10485760          # 10MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp

# Model Settings
DEFAULT_MODEL=ensemble          # ensemble | cnn | deepface | ...
CONFIDENCE_THRESHOLD=0.5        # 0.0 ~ 1.0
```

### 환경 변수 적용 확인

`DEBUG=true`로 설정하면 서버 시작 시 다음과 같이 출력됩니다:

```
[Database Config] Redis: localhost:6379/0
[Database Config] MongoDB: mongodb://localhost:27017 -> deep_guard.inference_results
[Database Config] Redis TTL: 86400s (24h)
```

## ⚡ 성능

### 응답 속도

| 작업 | 시간 | 설명 |
|------|------|------|
| Redis 캐시 히트 | ~10ms | 최근 조회한 결과 |
| MongoDB 조회 | ~50ms | DB에서 직접 조회 |
| Ensemble 추론 | ~400ms | CNN + DeepFace + FaceRec |
| CNN 단독 | ~50ms | 가장 빠른 탐지 |
| DeepFace 단독 | ~200ms | 감정 분석 포함 |

### 메모리 사용량

- 서버 기본: ~200MB
- AI 모델 로딩 후: ~1.5GB
- Redis 캐시 (1000건): ~50MB
- MongoDB 저장소 (10000건): ~100MB

### 처리량 (Throughput)

- 캐시 히트: ~1000 req/s
- DB 조회: ~200 req/s
- 추론 + 저장: ~2.5 req/s (병렬 처리 가능)

## 🔒 보안

- 파일 업로드 크기 제한 (10MB)
- 허용된 확장자만 처리 (jpg, jpeg, png, webp)
- CORS 설정으로 허가된 도메인만 접근
- Redis 비밀번호 설정 지원
- MongoDB 인증 지원

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

```bash
git checkout -b feat/amazing-feature
git commit -m 'feat: Add amazing feature'
git push origin feat/amazing-feature
```

## 👨‍💻 제작

**Created by**: [@hwnnn](https://github.com/hwnnn)  
**Repository**: [deep_guard](https://github.com/hwnnn/deep_guard)

---

**Technology Stack**: FastAPI · Redis · MongoDB · DeepFace · InsightFace · Docker