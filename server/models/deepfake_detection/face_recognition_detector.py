from io import BytesIO
from PIL import Image
import numpy as np
import cv2
from typing import Dict, Any
from .base import DeepfakeDetectorModel


class FaceRecognitionDetector(DeepfakeDetectorModel):
    """
    face_recognition + dlib을 활용한 딥페이크 탐지
    얼굴 랜드마크 분석을 통한 정밀한 탐지
    """
    
    def __init__(self):
        self.name = "face_recognition_detector_v1"
        self.threshold = 0.5
        
    def detect(self, image_bytes: bytes) -> Dict[str, Any]:
        try:
            import face_recognition
            
            # 이미지 로드
            img = Image.open(BytesIO(image_bytes)).convert("RGB")
            img_array = np.array(img)
            
            # 얼굴 위치 탐지
            face_locations = face_recognition.face_locations(img_array, model="hog")
            
            if not face_locations:
                return {
                    "is_fake": False,
                    "confidence": 0.3,
                    "fake_probability": 0.3,
                    "real_probability": 0.7,
                    "suspicious_regions": [],
                    "analysis": {"error": "No face detected"},
                    "model": "face_recognition"
                }
            
            # 얼굴 랜드마크 탐지
            face_landmarks_list = face_recognition.face_landmarks(img_array, face_locations)
            
            # 얼굴 인코딩 (128차원 벡터)
            face_encodings = face_recognition.face_encodings(img_array, face_locations)
            
            # 딥페이크 특징 분석
            fake_score = self._analyze_face_features(
                img_array, 
                face_locations, 
                face_landmarks_list,
                face_encodings
            )
            
            fake_probability = float(fake_score)
            real_probability = 1.0 - fake_probability
            is_fake = fake_probability > self.threshold
            
            # 의심 영역 생성
            suspicious_regions = []
            for (top, right, bottom, left) in face_locations:
                suspicious_regions.append({
                    "x": int(left),
                    "y": int(top),
                    "width": int(right - left),
                    "height": int(bottom - top),
                    "type": "face",
                    "confidence": float(fake_probability)
                })
            
            # 랜드마크 분석
            landmark_analysis = {}
            if face_landmarks_list:
                landmarks = face_landmarks_list[0]
                landmark_analysis = {
                    "chin_points": len(landmarks.get('chin', [])),
                    "left_eye_points": len(landmarks.get('left_eye', [])),
                    "right_eye_points": len(landmarks.get('right_eye', [])),
                    "nose_points": len(landmarks.get('nose_bridge', [])) + len(landmarks.get('nose_tip', [])),
                    "mouth_points": len(landmarks.get('top_lip', [])) + len(landmarks.get('bottom_lip', []))
                }
            
            return {
                "is_fake": bool(is_fake),
                "confidence": float(max(fake_probability, real_probability)),
                "fake_probability": fake_probability,
                "real_probability": real_probability,
                "suspicious_regions": suspicious_regions,
                "analysis": {
                    "faces_detected": len(face_locations),
                    "landmark_quality": self._calculate_landmark_quality(face_landmarks_list),
                    "encoding_consistency": self._check_encoding_consistency(face_encodings),
                    "landmarks": landmark_analysis
                },
                "model": "face_recognition + dlib"
            }
            
        except Exception as e:
            return self._fallback_detection(str(e))
    
    def _analyze_face_features(
        self, 
        img_array: np.ndarray,
        face_locations: list,
        face_landmarks_list: list,
        face_encodings: list
    ) -> float:
        """얼굴 특징 분석으로 딥페이크 점수 계산"""
        score = 0.0
        
        # 1. 랜드마크 대칭성 검사
        if face_landmarks_list:
            symmetry_score = self._check_facial_symmetry(face_landmarks_list[0])
            if symmetry_score < 0.7:  # 비대칭
                score += 0.25
        
        # 2. 랜드마크 일관성
        if face_landmarks_list:
            consistency = self._check_landmark_consistency(face_landmarks_list[0])
            if consistency < 0.8:
                score += 0.2
        
        # 3. 얼굴 인코딩 품질
        if face_encodings:
            encoding_quality = np.linalg.norm(face_encodings[0])
            if encoding_quality < 5.0 or encoding_quality > 15.0:  # 비정상 범위
                score += 0.15
        
        # 4. 얼굴 영역 품질
        for (top, right, bottom, left) in face_locations:
            face_region = img_array[top:bottom, left:right]
            if face_region.size > 0:
                # 블러 검출
                gray_face = cv2.cvtColor(face_region, cv2.COLOR_RGB2GRAY)
                blur = cv2.Laplacian(gray_face, cv2.CV_64F).var()
                if blur < 100:
                    score += 0.2
        
        # 5. 얼굴 크기 일관성
        if len(face_locations) > 1:
            sizes = [(right - left) * (bottom - top) for (top, right, bottom, left) in face_locations]
            size_variance = np.var(sizes) / (np.mean(sizes) + 1e-7)
            if size_variance > 0.5:  # 크기 차이가 큼
                score += 0.2
        
        return min(score, 1.0)
    
    def _check_facial_symmetry(self, landmarks: Dict) -> float:
        """얼굴 대칭성 검사"""
        try:
            left_eye = np.array(landmarks.get('left_eye', []))
            right_eye = np.array(landmarks.get('right_eye', []))
            
            if len(left_eye) == 0 or len(right_eye) == 0:
                return 0.5
            
            # 눈 중심점 계산
            left_center = left_eye.mean(axis=0)
            right_center = right_eye.mean(axis=0)
            
            # 대칭축과의 거리 비교
            chin = landmarks.get('chin', [])
            if chin:
                face_center_x = np.mean([p[0] for p in chin])
                left_dist = abs(left_center[0] - face_center_x)
                right_dist = abs(right_center[0] - face_center_x)
                
                symmetry = 1.0 - abs(left_dist - right_dist) / (left_dist + right_dist + 1e-7)
                return float(symmetry)
            
            return 0.7
        except:
            return 0.5
    
    def _check_landmark_consistency(self, landmarks: Dict) -> float:
        """랜드마크 일관성 검사"""
        try:
            # 모든 랜드마크가 존재하는지 확인
            required_features = ['chin', 'left_eye', 'right_eye', 'nose_bridge', 'top_lip', 'bottom_lip']
            present = sum(1 for feature in required_features if landmarks.get(feature))
            consistency = present / len(required_features)
            return float(consistency)
        except:
            return 0.5
    
    def _calculate_landmark_quality(self, face_landmarks_list: list) -> float:
        """랜드마크 품질 계산"""
        if not face_landmarks_list:
            return 0.0
        
        landmarks = face_landmarks_list[0]
        total_points = sum(len(points) for points in landmarks.values())
        expected_points = 68  # dlib 68-point model
        
        return min(total_points / expected_points, 1.0)
    
    def _check_encoding_consistency(self, face_encodings: list) -> float:
        """얼굴 인코딩 일관성 검사"""
        if not face_encodings:
            return 0.0
        
        encoding = face_encodings[0]
        # 인코딩 벡터의 분산이 적절한지 확인
        variance = np.var(encoding)
        
        # 정상 범위: 0.01 ~ 0.1
        if 0.01 <= variance <= 0.1:
            return 1.0
        elif variance < 0.01:
            return 0.5  # 너무 일정함
        else:
            return 0.3  # 너무 변동이 큼
    
    def _fallback_detection(self, error: str) -> Dict[str, Any]:
        """face_recognition 실패 시 대체 탐지"""
        return {
            "is_fake": False,
            "confidence": 0.3,
            "fake_probability": 0.3,
            "real_probability": 0.7,
            "suspicious_regions": [],
            "analysis": {
                "error": f"face_recognition analysis failed: {error}",
                "fallback": True
            },
            "model": "face_recognition (Fallback)"
        }
