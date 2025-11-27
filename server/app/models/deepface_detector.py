from io import BytesIO
from PIL import Image
import numpy as np
import cv2
from typing import Dict, Any
from .base import DeepfakeDetectorModel


class DeepFaceDetector(DeepfakeDetectorModel):
    """
    DeepFace 라이브러리를 활용한 딥페이크 탐지
    얼굴 인식, 감정 분석, 연령/성별 추정을 통한 딥페이크 탐지
    """
    
    def __init__(self):
        self.name = "deepface_detector_v1"
        self.threshold = 0.5
        
    def detect(self, image_bytes: bytes) -> Dict[str, Any]:
        try:
            from deepface import DeepFace
            
            # 이미지 로드
            img = Image.open(BytesIO(image_bytes)).convert("RGB")
            img_array = np.array(img)
            
            # 임시 파일로 저장 (DeepFace는 파일 경로를 요구)
            import tempfile
            import os
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                img.save(tmp.name)
                temp_path = tmp.name
            
            try:
                # 얼굴 분석 수행
                analysis = DeepFace.analyze(
                    img_path=temp_path,
                    actions=['emotion', 'age', 'gender', 'race'],
                    enforce_detection=False
                )
                
                # 여러 얼굴이 탐지된 경우 첫 번째만 사용
                if isinstance(analysis, list):
                    analysis = analysis[0]
                
                # 딥페이크 특징 분석
                fake_score = self._analyze_deepface_features(analysis, img_array)
                
                fake_probability = float(fake_score)
                real_probability = 1.0 - fake_probability
                is_fake = fake_probability > self.threshold
                
                # 얼굴 영역 정보
                region = analysis.get('region', {})
                suspicious_regions = []
                if region:
                    suspicious_regions.append({
                        "x": int(region.get('x', 0)),
                        "y": int(region.get('y', 0)),
                        "width": int(region.get('w', 0)),
                        "height": int(region.get('h', 0)),
                        "type": "face",
                        "confidence": float(fake_probability)
                    })
                
                return {
                    "is_fake": bool(is_fake),
                    "confidence": float(max(fake_probability, real_probability)),
                    "fake_probability": fake_probability,
                    "real_probability": real_probability,
                    "suspicious_regions": suspicious_regions,
                    "analysis": {
                        "dominant_emotion": analysis.get('dominant_emotion', 'unknown'),
                        "age": int(analysis.get('age', 0)),
                        "gender": analysis.get('dominant_gender', 'unknown'),
                        "race": analysis.get('dominant_race', 'unknown'),
                        "emotion_confidence": float(max(analysis.get('emotion', {}).values()) if analysis.get('emotion') else 0)
                    },
                    "model": "DeepFace"
                }
                
            finally:
                # 임시 파일 삭제
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            # DeepFace 실패 시 기본 분석
            return self._fallback_detection(image_bytes, str(e))
    
    def _analyze_deepface_features(self, analysis: Dict, img_array: np.ndarray) -> float:
        """DeepFace 분석 결과로 딥페이크 점수 계산"""
        score = 0.0
        
        # 1. 감정 분석 - 딥페이크는 감정 표현이 부자연스러움
        emotions = analysis.get('emotion', {})
        if emotions:
            emotion_variance = np.var(list(emotions.values()))
            if emotion_variance < 100:  # 감정 분포가 평평함
                score += 0.2
        
        # 2. 연령 추정 - 딥페이크는 실제 나이와 불일치 가능
        age = analysis.get('age', 0)
        if age < 18 or age > 70:  # 극단적인 나이
            score += 0.1
        
        # 3. 얼굴 검출 신뢰도
        region = analysis.get('region', {})
        if not region or region.get('w', 0) < 50:  # 얼굴이 너무 작음
            score += 0.15
        
        # 4. 이미지 품질 분석
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        if blur_score < 100:  # 이미지가 흐림
            score += 0.15
        
        return min(score, 1.0)
    
    def _fallback_detection(self, image_bytes: bytes, error: str) -> Dict[str, Any]:
        """DeepFace 실패 시 대체 탐지"""
        return {
            "is_fake": False,
            "confidence": 0.3,
            "fake_probability": 0.3,
            "real_probability": 0.7,
            "suspicious_regions": [],
            "analysis": {
                "error": f"DeepFace analysis failed: {error}",
                "fallback": True
            },
            "model": "DeepFace (Fallback)"
        }
