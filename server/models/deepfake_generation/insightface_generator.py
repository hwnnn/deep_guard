from io import BytesIO
from PIL import Image
import numpy as np
import cv2
from typing import Dict, Any, Optional
from .base import DeepfakeGeneratorModel


class InsightFaceGenerator(DeepfakeGeneratorModel):
    """
    InsightFace를 활용한 고급 딥페이크 생성
    ONNX 기반 빠른 추론 및 높은 품질의 얼굴 스왑
    """
    
    def __init__(self):
        self.name = "insightface_generator_v1"
        self.app = None
        self.swapper = None
        
    def _initialize_models(self):
        """InsightFace 모델 초기화 (lazy loading)"""
        if self.app is None:
            try:
                import insightface
                from insightface.app import FaceAnalysis
                
                # FaceAnalysis 초기화 (얼굴 탐지 및 분석)
                self.app = FaceAnalysis(name='buffalo_l')
                self.app.prepare(ctx_id=0, det_size=(640, 640))
                
                print("✅ InsightFace 모델 로드 완료")
                
            except Exception as e:
                print(f"⚠️ InsightFace 초기화 실패: {str(e)}")
                raise
    
    def generate(self, source_bytes: bytes, target_bytes: bytes) -> Dict[str, Any]:
        """
        InsightFace를 사용한 얼굴 스왑 생성
        
        Args:
            source_bytes: 스왑할 원본 얼굴 이미지
            target_bytes: 타겟 이미지 (얼굴이 교체될 이미지)
            
        Returns:
            생성된 딥페이크 이미지 정보
        """
        try:
            # 모델 초기화
            self._initialize_models()
            
            # 이미지 로드
            source_img = Image.open(BytesIO(source_bytes)).convert("RGB")
            target_img = Image.open(BytesIO(target_bytes)).convert("RGB")
            
            source_array = np.array(source_img)
            target_array = np.array(target_img)
            
            # RGB -> BGR (OpenCV 형식)
            source_bgr = cv2.cvtColor(source_array, cv2.COLOR_RGB2BGR)
            target_bgr = cv2.cvtColor(target_array, cv2.COLOR_RGB2BGR)
            
            # 얼굴 탐지 및 분석
            source_faces = self.app.get(source_bgr)
            target_faces = self.app.get(target_bgr)
            
            if not source_faces:
                return {
                    "success": False,
                    "error": "No face detected in source image",
                    "model": "insightface",
                    "source_faces": 0,
                    "target_faces": len(target_faces)
                }
            
            if not target_faces:
                return {
                    "success": False,
                    "error": "No face detected in target image",
                    "model": "insightface",
                    "source_faces": len(source_faces),
                    "target_faces": 0
                }
            
            # 얼굴 스왑 수행
            result_img = self._swap_faces(
                source_bgr, 
                target_bgr, 
                source_faces[0], 
                target_faces
            )
            
            # BGR -> RGB
            result_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            
            # 결과 이미지를 바이트로 변환
            result_pil = Image.fromarray(result_rgb)
            output_buffer = BytesIO()
            result_pil.save(output_buffer, format='JPEG', quality=95)
            result_bytes = output_buffer.getvalue()
            
            # 분석 정보
            analysis = self._analyze_faces(source_faces, target_faces)
            
            return {
                "success": True,
                "image_bytes": result_bytes,
                "format": "JPEG",
                "model": "insightface",
                "source_faces": len(source_faces),
                "target_faces": len(target_faces),
                "swapped_faces": len(target_faces),
                "analysis": analysis
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "model": "insightface"
            }
    
    def _swap_faces(self, source_img, target_img, source_face, target_faces):
        """
        실제 얼굴 스왑 수행
        """
        import insightface
        from insightface.model_zoo import get_model
        
        # Face Swapper 모델 로드 (첫 실행 시)
        if self.swapper is None:
            try:
                self.swapper = get_model('inswapper_128.onnx', download=True, download_zip=True)
            except Exception as e:
                print(f"⚠️ Swapper 모델 로드 실패, 대체 방법 사용: {str(e)}")
                return self._manual_face_swap(source_img, target_img, source_face, target_faces[0])
        
        # 결과 이미지 (타겟 이미지의 복사본)
        result = target_img.copy()
        
        # 모든 타겟 얼굴에 대해 스왑 수행
        for target_face in target_faces:
            try:
                result = self.swapper.get(result, target_face, source_face, paste_back=True)
            except Exception as e:
                print(f"⚠️ 스왑 실패, 대체 방법 사용: {str(e)}")
                result = self._manual_face_swap(source_img, result, source_face, target_face)
        
        return result
    
    def _manual_face_swap(self, source_img, target_img, source_face, target_face):
        """
        수동 얼굴 스왑 (InsightFace 모델 사용 불가 시)
        얼굴 랜드마크를 사용한 기본 스왑
        """
        result = target_img.copy()
        
        # 얼굴 바운딩 박스
        src_bbox = source_face.bbox.astype(int)
        tgt_bbox = target_face.bbox.astype(int)
        
        # 바운딩 박스 확장 (더 자연스러운 블렌딩)
        src_x1, src_y1, src_x2, src_y2 = src_bbox
        tgt_x1, tgt_y1, tgt_x2, tgt_y2 = tgt_bbox
        
        # 여유 공간 추가
        margin = 0.2
        src_w, src_h = src_x2 - src_x1, src_y2 - src_y1
        tgt_w, tgt_h = tgt_x2 - tgt_x1, tgt_y2 - tgt_y1
        
        src_x1 = max(0, int(src_x1 - src_w * margin))
        src_y1 = max(0, int(src_y1 - src_h * margin))
        src_x2 = min(source_img.shape[1], int(src_x2 + src_w * margin))
        src_y2 = min(source_img.shape[0], int(src_y2 + src_h * margin))
        
        tgt_x1 = max(0, int(tgt_x1 - tgt_w * margin))
        tgt_y1 = max(0, int(tgt_y1 - tgt_h * margin))
        tgt_x2 = min(target_img.shape[1], int(tgt_x2 + tgt_w * margin))
        tgt_y2 = min(target_img.shape[0], int(tgt_y2 + tgt_h * margin))
        
        # 얼굴 영역 추출
        source_face_region = source_img[src_y1:src_y2, src_x1:src_x2]
        
        # 타겟 크기로 리사이즈
        target_size = (tgt_x2 - tgt_x1, tgt_y2 - tgt_y1)
        if target_size[0] > 0 and target_size[1] > 0:
            resized_face = cv2.resize(source_face_region, target_size)
            
            # 마스크 생성 (타원형)
            mask = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)
            center = (target_size[0] // 2, target_size[1] // 2)
            axes = (target_size[0] // 2 - 10, target_size[1] // 2 - 10)
            cv2.ellipse(mask, center, axes, 0, 0, 360, (255, 255, 255), -1)
            mask = cv2.GaussianBlur(mask, (21, 21), 11)
            
            # 색상 매칭 (LAB 색공간)
            target_region = result[tgt_y1:tgt_y2, tgt_x1:tgt_x2]
            resized_face = self._match_skin_tone(resized_face, target_region)
            
            # 블렌딩
            mask_float = mask.astype(float) / 255
            blended = (resized_face * mask_float + target_region * (1 - mask_float)).astype(np.uint8)
            
            # 결과에 반영
            result[tgt_y1:tgt_y2, tgt_x1:tgt_x2] = blended
        
        return result
    
    def _match_skin_tone(self, source, target):
        """LAB 색공간에서 피부톤 매칭"""
        source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
        target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB)
        
        source_mean = cv2.mean(source_lab)[:3]
        target_mean = cv2.mean(target_lab)[:3]
        
        # L, A, B 채널 조정
        adjusted = source_lab.copy()
        for i in range(3):
            adjusted[:, :, i] = np.clip(
                adjusted[:, :, i] + (target_mean[i] - source_mean[i]),
                0, 255
            ).astype(np.uint8)
        
        return cv2.cvtColor(adjusted, cv2.COLOR_LAB2BGR)
    
    def _analyze_faces(self, source_faces, target_faces):
        """얼굴 분석 정보 추출"""
        analysis = {
            "source_info": [],
            "target_info": []
        }
        
        # 소스 얼굴 정보
        for face in source_faces:
            info = {
                "bbox": face.bbox.tolist(),
                "confidence": float(face.det_score),
                "age": int(face.age) if hasattr(face, 'age') else None,
                "gender": face.gender if hasattr(face, 'gender') else None,
                "embedding_size": face.embedding.shape[0] if hasattr(face, 'embedding') else None
            }
            analysis["source_info"].append(info)
        
        # 타겟 얼굴 정보
        for face in target_faces:
            info = {
                "bbox": face.bbox.tolist(),
                "confidence": float(face.det_score),
                "age": int(face.age) if hasattr(face, 'age') else None,
                "gender": face.gender if hasattr(face, 'gender') else None,
                "embedding_size": face.embedding.shape[0] if hasattr(face, 'embedding') else None
            }
            analysis["target_info"].append(info)
        
        return analysis
