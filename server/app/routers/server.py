from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ..dependencies import get_deepfake_detector
from ..database import get_db, DatabaseManager
import uuid
from datetime import datetime

router = APIRouter(prefix="/inference", tags=["inference"])


@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_file_for_inference(
    file: UploadFile = File(...),
    detector=Depends(get_deepfake_detector),
    db: DatabaseManager = Depends(get_db)
):
    """
    프론트엔드에서 이미지 파일을 업로드하여 딥페이크 탐지를 수행합니다.
    
    - **file**: 탐지할 이미지 파일
    
    Returns:
        - task_id: 추론 결과를 조회할 수 있는 고유 ID
        - status: 처리 상태 ("success")
        - message: 처리 결과 메시지
    """
    try:
        # 파일명 검증
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required"
            )
        
        # 파일 확장자 검증
        allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        filename_lower = file.filename.lower()
        file_ext = filename_lower[filename_lower.rfind("."):] if "." in filename_lower else ""
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # 이미지 파일 읽기
        image_bytes = await file.read()
        
        # 파일 크기 검증 (10MB 제한)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(image_bytes) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large. Maximum size: 10MB"
            )
        
        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file uploaded"
            )
        
        # 딥페이크 탐지 수행
        result = detector.detect(image_bytes)
        
        # 고유 task_id 생성
        task_id = str(uuid.uuid4())
        
        # 결과 구성
        data = {
            "task_id": task_id,
            "filename": file.filename,
            "file_size": len(image_bytes),
            "timestamp": datetime.utcnow().isoformat(),
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
        
        # Redis (cache) + MongoDB (persistent) 저장
        await db.save(task_id, data)
        
        # 성공 응답
        return JSONResponse(
            content={
                "task_id": task_id,
                "status": "success",
                "message": "File uploaded and processed successfully"
            },
            status_code=status.HTTP_200_OK
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/result/{task_id}")
async def get_inference_result(
    task_id: str,
    db: DatabaseManager = Depends(get_db)
):
    """
    업로드한 파일의 딥페이크 탐지 결과를 조회합니다.
    Redis → MongoDB → Fallback 순서로 조회
    """
    try:
        result = await db.get(task_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Result not found for task_id: {task_id}"
            )
        
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving result: {str(e)}"
        )


@router.get("/statistics")
async def get_statistics(db: DatabaseManager = Depends(get_db)):
    """
    전체 추론 통계 조회 (MongoDB 필요)
    """
    try:
        stats = await db.stats()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Statistics unavailable (MongoDB not connected)"
            )
        
        return JSONResponse(content=stats, status_code=status.HTTP_200_OK)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )
