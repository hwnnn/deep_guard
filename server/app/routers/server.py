"""
Unified API Router for face swap inference.
Serves both web and mobile frontends with a single endpoint.
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from ..dependencies import get_face_swap_model
import base64

router = APIRouter(prefix="/inference", tags=["inference"])


def _is_image(upload: UploadFile) -> bool:
    """Validate that uploaded file has image content type."""
    ct = upload.content_type
    return bool(ct and ct.startswith("image"))


@router.post("/face-swap")
async def face_swap_inference(
    source: UploadFile = File(..., description="Source image (face to be swapped)"),
    target: UploadFile = File(..., description="Target image (base image)"),
    model=Depends(get_face_swap_model)
):
    """
    Face swap inference endpoint for both web and mobile clients.
    
    Accepts two image files:
    - source: The face image to extract features from
    - target: The base image where the face will be applied
    
    Returns:
    - result_image_base64: Base64-encoded JPEG of the swapped result
    - model: Name of the model used for inference
    """
    # Validate both files are images
    if not _is_image(source) or not _is_image(target):
        raise HTTPException(
            status_code=400, 
            detail="Both 'source' and 'target' must be valid image files"
        )
    
    # Read uploaded files as bytes
    source_bytes = await source.read()
    target_bytes = await target.read()
    
    # Run model inference
    result_bytes = model.swap(source_bytes, target_bytes)
    
    # Encode result as Base64 for JSON response
    result_base64 = base64.b64encode(result_bytes).decode("utf-8")
    
    return {
        "result_image_base64": result_base64,
        "model": getattr(model, "name", "unknown"),
        "status": "success"
    }
