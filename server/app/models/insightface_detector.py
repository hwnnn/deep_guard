from io import BytesIO
from PIL import Image
import numpy as np
import cv2
from typing import Dict, Any
from .base import DeepfakeDetectorModel


class InsightFaceDetector(DeepfakeDetectorModel):
    """
    InsightFace를 활용한 딥페이크 탐지
    얼굴 임베딩 일관성, 품질 점수, 랜드마크 분석을 통한 탐지
    """
    
    def __init__(self):
        self.name = "insightface_detector_v1"
        self.threshold = 0.5
        self.app = None
        
    def _initialize_model(self):
        """InsightFace 모델 초기화 (lazy loading)"""
        if self.app is None:
            try:
                from insightface.app import FaceAnalysis
                
                # FaceAnalysis 초기화
                self.app = FaceAnalysis(name='buffalo_l')
                self.app.prepare(ctx_id=0, det_size=(640, 640))
                
                print("✅ InsightFace Detector 로드 완료")
                
            except Exception as e:
                print(f"⚠️ InsightFace 초기화 실패: {str(e)}")
                raise
    
    def detect(self, image_bytes: bytes) -> Dict[str, Any]:
        try:
            # 모델 초기화
            self._initialize_model()
            
            # 이미지 로드
            img = Image.open(BytesIO(image_bytes)).convert("RGB")
            img_array = np.array(img)
            
            # RGB -> BGR
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # 얼굴 탐지 및 분석
            faces = self.app.get(img_bgr)
            
            if not faces:
                return {
                    "is_fake": False,
                    "confidence": 0.3,
                    "fake_probability": 0.3,
                    "real_probability": 0.7,
                    "suspicious_regions": [],
                    "analysis": {"error": "No face detected"},
                    "model": "insightface"
                }
            
            # 딥페이크 특징 분석
            fake_score = self._analyze_insightface_features(faces, img_bgr)
            
            fake_probability = float(fake_score)
            real_probability = 1.0 - fake_probability
            is_fake = fake_probability >= self.threshold
            
            # 의심 영역 추출
            suspicious_regions = []
            for face in faces:
                if face.det_score < 0.9:  # 낮은 탐지 신뢰도는 의심스러움
                    bbox = face.bbox.astype(int)
                    suspicious_regions.append({
                        "x": int(bbox[0]),
                        "y": int(bbox[1]),
                        "width": int(bbox[2] - bbox[0]),
                        "height": int(bbox[3] - bbox[1]),
                        "confidence": float(face.det_score)
                    })
            
            # 상세 분석 정보
            analysis = self._get_detailed_analysis(faces, fake_score)
            
            return {
                "is_fake": is_fake,
                "confidence": max(real_probability, fake_probability),
                "fake_probability": fake_probability,
                "real_probability": real_probability,
                "suspicious_regions": suspicious_regions,
                "analysis": analysis,
                "model": "insightface"
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "is_fake": False,
                "confidence": 0.3,
                "fake_probability": 0.3,
                "real_probability": 0.7,
                "suspicious_regions": [],
                "analysis": {"error": str(e)},
                "model": "insightface"
            }
    
    def _analyze_insightface_features(self, faces, img_bgr):
        """
        InsightFace 특징을 기반으로 딥페이크 점수 계산
        """
        fake_indicators = []
        
        for face in faces:
            # 1. 탐지 신뢰도 (낮으면 의심스러움)
            detection_quality = face.det_score
            if detection_quality < 0.95:
                fake_indicators.append(1.0 - detection_quality)
            
            # 2. 얼굴 품질 점수
            if hasattr(face, 'pose'):
                # 포즈 각도 분석 (극단적인 각도는 의심스러움)
                pose = face.pose
                if pose is not None:
                    pitch, yaw, roll = pose
                    max_angle = max(abs(pitch), abs(yaw), abs(roll))
                    if max_angle > 30:  # 30도 이상 회전
                        fake_indicators.append(max_angle / 90.0)
            
            # 3. 임베딩 일관성 (여러 얼굴이 있을 때)
            if len(faces) > 1 and hasattr(face, 'embedding'):
                # 다른 얼굴과의 유사도 계산
                embedding = face.embedding
                for other_face in faces:
                    if other_face is not face and hasattr(other_face, 'embedding'):
                        similarity = self._cosine_similarity(embedding, other_face.embedding)
                        if similarity > 0.9:  # 너무 유사하면 복제 가능성
                            fake_indicators.append(similarity - 0.8)
            
            # 4. 랜드마크 품질
            if hasattr(face, 'kps'):
                landmark_quality = self._analyze_landmark_quality(face.kps)
                if landmark_quality < 0.8:
                    fake_indicators.append(1.0 - landmark_quality)
            
            # 5. 나이/성별 신뢰도
            if hasattr(face, 'age') and hasattr(face, 'gender'):
                # 극단적인 나이는 의심스러울 수 있음
                age = face.age
                if age < 10 or age > 90:
                    fake_indicators.append(0.3)
        
        # 평균 가짜 점수 계산
        if fake_indicators:
            fake_score = np.mean(fake_indicators)
        else:
            fake_score = 0.0
        
        # 기본 바이어스: 딥페이크가 아닐 확률이 높음
        fake_score = min(fake_score + 0.1, 1.0)
        
        return fake_score
    
    def _cosine_similarity(self, emb1, emb2):
        """코사인 유사도 계산"""
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
    
    def _analyze_landmark_quality(self, landmarks):
        """
        랜드마크 품질 분석
        landmarks: (5, 2) 형태의 배열 (좌눈, 우눈, 코, 좌입, 우입)
        """
        if landmarks is None or len(landmarks) < 5:
            return 0.5
        
        # 1. 좌우 대칭성 검사
        left_eye = landmarks[0]
        right_eye = landmarks[1]
        left_mouth = landmarks[3]
        right_mouth = landmarks[4]
        
        # 눈 사이 거리와 입 사이 거리 비율
        eye_distance = np.linalg.norm(left_eye - right_eye)
        mouth_distance = np.linalg.norm(left_mouth - right_mouth)
        
        if eye_distance > 0:
            ratio = mouth_distance / eye_distance
            # 일반적인 비율: 0.5 ~ 0.8
            if 0.4 < ratio < 0.9:
                symmetry_score = 1.0
            else:
                symmetry_score = 0.5
        else:
            symmetry_score = 0.5
        
        # 2. 랜드마크 간 거리의 일관성
        nose = landmarks[2]
        nose_to_left_eye = np.linalg.norm(nose - left_eye)
        nose_to_right_eye = np.linalg.norm(nose - right_eye)
        
        if max(nose_to_left_eye, nose_to_right_eye) > 0:
            nose_symmetry = min(nose_to_left_eye, nose_to_right_eye) / max(nose_to_left_eye, nose_to_right_eye)
        else:
            nose_symmetry = 0.5
        
        # 종합 품질 점수
        quality_score = (symmetry_score + nose_symmetry) / 2.0
        
        return quality_score
    
    def _get_detailed_analysis(self, faces, fake_score):
        """상세 분석 정보 반환"""
        analysis = {
            "faces_detected": len(faces),
            "average_fake_score": float(fake_score),
            "faces_info": []
        }
        
        for i, face in enumerate(faces):
            face_info = {
                "face_index": i,
                "bbox": face.bbox.tolist(),
                "detection_confidence": float(face.det_score),
            }
            
            if hasattr(face, 'age'):
                face_info["age"] = int(face.age)
            
            if hasattr(face, 'gender'):
                face_info["gender"] = "Male" if face.gender == 1 else "Female"
            
            if hasattr(face, 'pose'):
                pose = face.pose
                if pose is not None:
                    face_info["pose"] = {
                        "pitch": float(pose[0]),
                        "yaw": float(pose[1]),
                        "roll": float(pose[2])
                    }
            
            if hasattr(face, 'kps'):
                face_info["landmark_points"] = face.kps.shape[0]
            
            if hasattr(face, 'embedding'):
                face_info["embedding_size"] = face.embedding.shape[0]
            
            analysis["faces_info"].append(face_info)
        
        return analysis
