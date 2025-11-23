from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from ..dependencies import get_deepfake_detector

router = APIRouter(prefix="/inference", tags=["inference"])


@router.post("/upload-file")
async def detect_deepfake(
    file: UploadFile = File(..., description="Image file to detect deepfake (jpeg, jpg, png)"),
    detector=Depends(get_deepfake_detector)
):
    """
    사용자가 업로드한 이미지에서 딥페이크를 탐지합니다.
    
    - **file**: 탐지할 이미지 파일 (jpeg, jpg, png 등)
    
    Returns:
        - is_fake: 딥페이크 여부 (boolean)
        - confidence: 신뢰도 (0~1)
        - fake_probability: 가짜일 확률 (0~1)
        - real_probability: 진짜일 확률 (0~1)
        - suspicious_regions: 의심스러운 영역 좌표 리스트
        - analysis: 상세 분석 정보
        - model: 사용된 모델 이름
    """
    try:
        # 파일 확장자 검증
        allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        file_ext = file.filename.lower()[file.filename.rfind("."):]
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # 이미지 파일 읽기
        image_bytes = await file.read()
        
        # 파일 크기 검증 (10MB 제한)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(image_bytes) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: 10MB"
            )
        
        # 딥페이크 탐지 수행
        result = detector.detect(image_bytes)
        
        # 응답 구성
        response = {
            "success": True,
            "filename": file.filename,
            "file_size": len(image_bytes),
            "detection_result": {
                "is_fake": result["is_fake"],
                "confidence": result["confidence"],
                "fake_probability": result["fake_probability"],
                "real_probability": result["real_probability"],
                "verdict": "🚨 DEEPFAKE DETECTED" if result["is_fake"] else "✓ AUTHENTIC IMAGE"
            },
            "suspicious_regions": result["suspicious_regions"],
            "analysis": result.get("analysis", {}),
            "model_info": {
                "name": result.get("model", "ensemble"),
                "type": "Ensemble Detector (CNN + DeepFace + FaceRecognition)"
            }
        }
        
        return JSONResponse(content=response, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )
