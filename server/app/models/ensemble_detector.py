from io import BytesIO
from PIL import Image
import numpy as np
from typing import Dict, Any, List
from .base import DeepfakeDetectorModel


class EnsembleDetector(DeepfakeDetectorModel):
    """
    앙상블 탐지기: 여러 모델의 결과를 종합하여 최종 판정
    CNN, DeepFace, face_recognition 모델을 모두 사용
    """
    
    def __init__(self):
        self.name = "ensemble_detector_v1"
        self.threshold = 0.5
        self.models = []
        
        # 모든 탐지 모델 초기화
        try:
            from .cnn_detector import CNNDeepfakeDetector
            self.models.append(("CNN", CNNDeepfakeDetector()))
        except Exception as e:
            print(f"CNN Detector failed to load: {e}")
        
        try:
            from .deepface_detector import DeepFaceDetector
            self.models.append(("DeepFace", DeepFaceDetector()))
        except Exception as e:
            print(f"DeepFace Detector failed to load: {e}")
        
        try:
            from .face_recognition_detector import FaceRecognitionDetector
            self.models.append(("FaceRecognition", FaceRecognitionDetector()))
        except Exception as e:
            print(f"FaceRecognition Detector failed to load: {e}")
    
    def detect(self, image_bytes: bytes) -> Dict[str, Any]:
        """앙상블 탐지 수행"""
        results = []
        errors = []
        
        # 각 모델로 탐지 수행
        for model_name, model in self.models:
            try:
                result = model.detect(image_bytes)
                result['model_name'] = model_name
                results.append(result)
            except Exception as e:
                errors.append(f"{model_name}: {str(e)}")
        
        if not results:
            return {
                "is_fake": False,
                "confidence": 0.0,
                "fake_probability": 0.0,
                "real_probability": 1.0,
                "suspicious_regions": [],
                "analysis": {
                    "error": "All models failed",
                    "errors": errors
                },
                "model": "Ensemble (Failed)"
            }
        
        # 앙상블 결과 계산
        fake_probs = [r['fake_probability'] for r in results]
        
        # 가중 평균 (각 모델의 confidence를 가중치로 사용)
        weights = [r['confidence'] for r in results]
        total_weight = sum(weights)
        
        if total_weight > 0:
            weighted_fake_prob = sum(p * w for p, w in zip(fake_probs, weights)) / total_weight
        else:
            weighted_fake_prob = np.mean(fake_probs)
        
        # 투표 방식
        fake_votes = sum(1 for r in results if r['is_fake'])
        vote_ratio = fake_votes / len(results)
        
        # 최종 확률 (가중 평균 70%, 투표 30%)
        final_fake_prob = weighted_fake_prob * 0.7 + vote_ratio * 0.3
        final_real_prob = 1.0 - final_fake_prob
        is_fake = final_fake_prob > self.threshold
        
        # 모든 모델의 suspicious regions 통합
        all_regions = []
        for result in results:
            all_regions.extend(result.get('suspicious_regions', []))
        
        # 중복 제거 및 병합
        merged_regions = self._merge_overlapping_regions(all_regions)
        
        # 개별 모델 결과 요약
        model_results = {}
        for result in results:
            model_name = result.get('model_name', 'unknown')
            model_results[model_name] = {
                "fake_probability": result['fake_probability'],
                "is_fake": result['is_fake'],
                "confidence": result['confidence']
            }
        
        return {
            "is_fake": bool(is_fake),
            "confidence": float(max(final_fake_prob, final_real_prob)),
            "fake_probability": float(final_fake_prob),
            "real_probability": float(final_real_prob),
            "suspicious_regions": merged_regions[:10],  # 최대 10개
            "analysis": {
                "ensemble_method": "weighted_average_70_vote_30",
                "models_used": len(results),
                "fake_votes": fake_votes,
                "vote_ratio": float(vote_ratio),
                "model_results": model_results,
                "errors": errors if errors else None
            },
            "model": "Ensemble (CNN + DeepFace + FaceRecognition)"
        }
    
    def _merge_overlapping_regions(self, regions: List[Dict]) -> List[Dict]:
        """중복되는 영역 병합"""
        if not regions:
            return []
        
        # 신뢰도 기준으로 정렬
        sorted_regions = sorted(regions, key=lambda r: r.get('confidence', 0), reverse=True)
        
        merged = []
        used = set()
        
        for i, region1 in enumerate(sorted_regions):
            if i in used:
                continue
            
            # 겹치는 영역 찾기
            overlapping = [region1]
            for j, region2 in enumerate(sorted_regions[i+1:], start=i+1):
                if j in used:
                    continue
                
                if self._calculate_iou(region1, region2) > 0.3:  # 30% 이상 겹침
                    overlapping.append(region2)
                    used.add(j)
            
            # 병합된 영역 생성
            if overlapping:
                merged_region = self._merge_regions(overlapping)
                merged.append(merged_region)
        
        return merged
    
    def _calculate_iou(self, region1: Dict, region2: Dict) -> float:
        """IoU (Intersection over Union) 계산"""
        x1_1, y1_1 = region1['x'], region1['y']
        x2_1, y2_1 = x1_1 + region1['width'], y1_1 + region1['height']
        
        x1_2, y1_2 = region2['x'], region2['y']
        x2_2, y2_2 = x1_2 + region2['width'], y1_2 + region2['height']
        
        # 교집합
        x_left = max(x1_1, x1_2)
        y_top = max(y1_1, y1_2)
        x_right = min(x2_1, x2_2)
        y_bottom = min(y2_1, y2_2)
        
        if x_right < x_left or y_bottom < y_top:
            return 0.0
        
        intersection = (x_right - x_left) * (y_bottom - y_top)
        
        # 합집합
        area1 = region1['width'] * region1['height']
        area2 = region2['width'] * region2['height']
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0
    
    def _merge_regions(self, regions: List[Dict]) -> Dict:
        """여러 영역을 하나로 병합"""
        x_min = min(r['x'] for r in regions)
        y_min = min(r['y'] for r in regions)
        x_max = max(r['x'] + r['width'] for r in regions)
        y_max = max(r['y'] + r['height'] for r in regions)
        
        avg_confidence = np.mean([r.get('confidence', 0) for r in regions])
        
        return {
            "x": int(x_min),
            "y": int(y_min),
            "width": int(x_max - x_min),
            "height": int(y_max - y_min),
            "type": "merged_face",
            "confidence": float(avg_confidence),
            "merged_count": len(regions)
        }
