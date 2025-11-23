# deep_guard

> DeepFake Face Swap Detection & Testing Backend API

딥페이크 얼굴 합성(Face Swap) 탐지 및 테스트를 위한 FastAPI 기반 백엔드 서버입니다.  
현재는 **더미 모델**을 사용하여 이미지 업로드 → 모델 추론 → 결과 반환의 전체 파이프라인을 검증합니다.

## 📋 목차

- [주요 기능](#주요-기능)
- [프로젝트 구조](#프로젝트-구조)
- [설치 및 실행](#설치-및-실행)
- [API 사용법](#api-사용법)
- [실제 모델 연동 가이드](#실제-모델-연동-가이드)
- [개발 환경](#개발-환경)

## 🚀 주요 기능

- **통합 API 엔드포인트**: 웹/모바일 클라이언트 모두 단일 API로 처리
- **모듈화된 아키텍처**: 의존성 주입 패턴으로 모델 교체 용이
- **확장 가능한 설계**: 실제 딥페이크 모델로 쉽게 교체 가능한 인터페이스
- **CORS 지원**: 프론트엔드 개발 편의를 위한 Cross-Origin 설정
- **자동 문서화**: FastAPI 기본 제공 Swagger UI (`/docs`)

## 📁 프로젝트 구조

```
deep_guard/
├── app/
│   ├── main.py                 # FastAPI 앱 엔트리포인트 & 라우터 등록
│   ├── core_config.py          # 환경변수 기반 설정 관리
│   ├── dependencies.py         # 의존성 주입 (모델 인스턴스 제공)
│   ├── routers/
│   │   └── server.py           # 통합 추론 API 라우터
│   └── services/
│       └── face_swap/
│           ├── base.py         # FaceSwapModel 추상 인터페이스
│           └── dummy_model.py  # 더미 구현 (개발/테스트용)
├── tests/
│   └── test_health.py          # API 테스트
├── images/                     # 테스트용 이미지 (샘플)
├── requirements.txt            # Python 의존성
├── .gitignore
└── README.md
```

## ⚙️ 설치 및 실행

### 요구사항

- Python 3.11 이상
- pip & venv

### 설치

```bash
# 1. 저장소 클론
git clone https://github.com/hwnnn/deep_guard.git
cd deep_guard

# 2. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. 의존성 설치
pip install -r requirements.txt
```

### 실행

```bash
# 개발 모드 (자동 재시작)
uvicorn app.main:app --reload --port 8000

# 프로덕션 모드
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

서버가 실행되면:
- API: `http://localhost:8000`
- Swagger 문서: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 API 사용법

### 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| `GET` | `/` | 루트 (서비스 정보) |
| `GET` | `/health` | 헬스체크 |
| `POST` | `/api/inference/face-swap` | **Face Swap 추론** (웹/모바일 공통) |

### Face Swap API 상세

#### 요청

- **URL**: `POST /api/inference/face-swap`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `source` (file, required): 합성할 얼굴 이미지
  - `target` (file, required): 베이스 이미지 (얼굴이 들어갈 이미지)

#### cURL 예시

```bash
curl -X POST \
  -F "source=@images/deepfake.jpeg" \
  -F "target=@images/original.jpeg" \
  http://localhost:8000/api/inference/face-swap
```

#### Python 예시

```python
import requests
import base64

# 이미지 업로드
with open("source.jpg", "rb") as src, open("target.jpg", "rb") as tgt:
    files = {
        "source": ("source.jpg", src, "image/jpeg"),
        "target": ("target.jpg", tgt, "image/jpeg"),
    }
    response = requests.post(
        "http://localhost:8000/api/inference/face-swap",
        files=files
    )

# 응답 처리
data = response.json()
if data["status"] == "success":
    # Base64 디코딩 후 저장
    result_bytes = base64.b64decode(data["result_image_base64"])
    with open("result.jpg", "wb") as f:
        f.write(result_bytes)
    print(f"✅ 합성 완료! 사용 모델: {data['model']}")
```

#### 응답

```json
{
  "result_image_base64": "/9j/4AAQSkZJRg...",
  "model": "dummy",
  "status": "success"
}
```

- `result_image_base64`: JPEG 이미지의 Base64 인코딩 문자열
- `model`: 사용된 모델 이름
- `status`: 처리 상태 (`success` | `error`)

## 🔧 실제 모델 연동 가이드

현재는 `DummyFaceSwapModel`을 사용합니다. 이 모델은:
- 실제 얼굴 매핑을 수행하지 않음
- Source 이미지를 축소해 Target 이미지 좌측 상단에 단순 오버레이
- 개발/테스트 목적으로만 사용

### 실제 모델로 교체하기

#### 1단계: 새 모델 클래스 생성

`app/services/face_swap/` 에 새 파일 생성 (예: `insightface_model.py`):

```python
from .base import FaceSwapModel
import insightface
from io import BytesIO
from PIL import Image

class InsightFaceSwapModel(FaceSwapModel):
    def __init__(self):
        # 모델 초기화
        self.app = insightface.app.FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        self.swapper = insightface.model_zoo.get_model('inswapper_128.onnx')
        self.name = "insightface"

    def swap(self, source: bytes, target: bytes) -> bytes:
        # 바이트 → 이미지 변환
        source_img = Image.open(BytesIO(source))
        target_img = Image.open(BytesIO(target))
        
        # 얼굴 검출 및 스왑 (실제 구현)
        # ... InsightFace 로직 ...
        
        # 결과 → 바이트 변환
        output = BytesIO()
        result_img.save(output, format='JPEG')
        return output.getvalue()
```

#### 2단계: 의존성 교체

`app/dependencies.py` 수정:

```python
# from .services.face_swap.dummy_model import DummyFaceSwapModel
from .services.face_swap.insightface_model import InsightFaceSwapModel

# face_swap_model = DummyFaceSwapModel()
face_swap_model = InsightFaceSwapModel()
```

#### 3단계: 의존성 추가

`requirements.txt`에 추가:
```
insightface==0.7.3
onnxruntime==1.16.0
```

끝! 이제 실제 딥페이크 모델이 동작합니다. 🎉

## 🧪 개발 환경

### 테스트 실행

```bash
# 전체 테스트
pytest

# 간략 모드
pytest -q

# 특정 테스트만
pytest tests/test_health.py
```

### 환경변수 설정

`.env` 파일 생성 (선택사항):

```env
APP_NAME=deep_guard_backend
API_V1_PREFIX=/api
DEBUG=true
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 프로젝트 구조 원칙

- **의존성 주입**: 모델 교체 시 코드 변경 최소화
- **단일 책임**: 각 모듈은 하나의 역할만 수행
- **인터페이스 기반**: 추상 클래스로 계약 정의 후 구현

## 🚧 향후 개선 계획

### 단기 (v0.2)
- [ ] 실제 딥페이크 모델 통합 (InsightFace, Roop 등)
- [ ] 이미지 검증 강화 (크기, 포맷, 해상도 제한)
- [ ] 에러 핸들링 개선 (상세한 에러 메시지)

### 중기 (v0.3)
- [ ] 비동기 작업 큐 (Celery + Redis)
- [ ] 결과 이미지 클라우드 저장 (S3/GCS)
- [ ] 처리 진행률 추적 API
- [ ] JWT 인증 추가

### 장기 (v1.0)
- [ ] 딥페이크 탐지 모델 추가
- [ ] 배치 처리 지원
- [ ] 웹소켓 기반 실시간 알림
- [ ] Docker & Kubernetes 배포 설정
- [ ] 모니터링 & 로깅 (Prometheus, Grafana)

## 📝 라이선스

MIT License

## 👥 기여

이슈와 PR은 언제나 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feat/amazing-feature`)
3. Commit your Changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the Branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

---

**Created by**: [@hwnnn](https://github.com/hwnnn)  
**Repository**: [deep_guard](https://github.com/hwnnn/deep_guard)