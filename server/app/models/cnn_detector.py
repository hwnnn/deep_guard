from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np
import cv2
from .base import DeepfakeDetectorModel
from typing import Dict, Any


class CNNDeepfakeDetector(DeepfakeDetectorModel):
    """
    CNN 기반 딥페이크 탐지 모델
    실제로는 사전 학습된 모델을 사용해야 하지만, 
    현재는 이미지 분석 기법을 활용한 휴리스틱 방법 사용
    """
    
    def __init__(self):
        self.name = "cnn_detector_v1"
        self.threshold = 0.5
    
    def detect(self, image_bytes: bytes) -> Dict[str, Any]:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(img)
        
        # OpenCV 형식으로 변환
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # 여러 딥페이크 특징 분석
        texture_score = self._analyze_texture_consistency(img_cv)
        edge_score = self._analyze_edge_artifacts(img_cv)
        frequency_score = self._analyze_frequency_domain(img_cv)
        face_score = self._analyze_face_boundaries(img_cv)
        
        # 가중치 적용하여 최종 점수 계산
        fake_probability = (
            texture_score * 0.3 +
            edge_score * 0.25 +
            frequency_score * 0.25 +
            face_score * 0.2
        )
        
        real_probability = 1.0 - fake_probability
        is_fake = fake_probability > self.threshold
        
        # 의심스러운 영역 탐지
        suspicious_regions = self._detect_suspicious_regions(img_cv, fake_probability)
        
        return {
            "is_fake": bool(is_fake),
            "confidence": float(max(fake_probability, real_probability)),
            "fake_probability": float(fake_probability),
            "real_probability": float(real_probability),
            "suspicious_regions": suspicious_regions,
            "analysis": {
                "texture_consistency": float(1.0 - texture_score),
                "edge_quality": float(1.0 - edge_score),
                "frequency_anomaly": float(frequency_score),
                "face_boundary_quality": float(1.0 - face_score)
            }
        }
    
    def _analyze_texture_consistency(self, img: np.ndarray) -> float:
        """텍스처 일관성 분석 - 딥페이크는 종종 텍스처가 부자연스러움"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 로컬 바이너리 패턴 분석
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist.flatten() / hist.sum()
        
        # 엔트로피 계산
        entropy = -np.sum(hist * np.log2(hist + 1e-7))
        
        # 정규화 (높은 엔트로피 = 자연스러운 텍스처)
        normalized_score = 1.0 - min(entropy / 8.0, 1.0)
        return normalized_score
    
    def _analyze_edge_artifacts(self, img: np.ndarray) -> float:
        """엣지 아티팩트 분석 - 딥페이크는 경계에서 아티팩트 발생"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Canny 엣지 검출
        edges = cv2.Canny(gray, 100, 200)
        
        # 엣지 연속성 분석
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        eroded = cv2.erode(dilated, kernel, iterations=1)
        
        # 불연속적인 엣지 비율
        discontinuity = np.sum(edges != eroded) / edges.size
        
        return float(min(discontinuity * 10, 1.0))
    
    def _analyze_frequency_domain(self, img: np.ndarray) -> float:
        """주파수 도메인 분석 - 딥페이크는 특정 주파수 패턴을 가짐"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # FFT 변환
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)
        
        # 고주파 성분 분석
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        
        # 중심에서 거리별 주파수 분석
        high_freq_region = magnitude[crow-10:crow+10, ccol-10:ccol+10]
        low_freq_region = magnitude[0:20, 0:20]
        
        ratio = np.mean(high_freq_region) / (np.mean(low_freq_region) + 1e-7)
        
        # 비정상적인 비율은 딥페이크 가능성
        anomaly = abs(ratio - 1.0)
        return float(min(anomaly / 10, 1.0))
    
    def _analyze_face_boundaries(self, img: np.ndarray) -> float:
        """얼굴 경계 분석 - 얼굴 교체 시 경계가 부자연스러움"""
        # Haar Cascade로 얼굴 검출
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            return 0.3  # 얼굴 없음
        
        boundary_scores = []
        for (x, y, w, h) in faces:
            # 얼굴 경계 영역 분석
            padding = 10
            if y-padding >= 0 and x-padding >= 0:
                boundary_region = gray[
                    max(0, y-padding):min(gray.shape[0], y+h+padding),
                    max(0, x-padding):min(gray.shape[1], x+w+padding)
                ]
                face_region = gray[y:y+h, x:x+w]
                
                # 경계와 얼굴 영역의 밝기 차이 분석
                boundary_mean = np.mean(boundary_region)
                face_mean = np.mean(face_region)
                diff = abs(boundary_mean - face_mean) / 255.0
                
                boundary_scores.append(diff)
        
        return float(np.mean(boundary_scores)) if boundary_scores else 0.3
    
    def _detect_suspicious_regions(self, img: np.ndarray, fake_prob: float) -> list:
        """의심스러운 영역 탐지"""
        if fake_prob < 0.3:
            return []
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 얼굴 검출
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        suspicious_regions = []
        for (x, y, w, h) in faces:
            suspicious_regions.append({
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h),
                "type": "face",
                "confidence": float(fake_prob)
            })
        
        # 엣지 이상 영역 검출
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours[:5]:  # 상위 5개만
            area = cv2.contourArea(contour)
            if area > 1000:  # 충분히 큰 영역만
                x, y, w, h = cv2.boundingRect(contour)
                suspicious_regions.append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "type": "edge_artifact",
                    "confidence": float(min(fake_prob * 0.8, 1.0))
                })
        
        return suspicious_regions[:10]  # 최대 10개 영역
