#!/usr/bin/env python3
"""
모든 딥페이크 탐지 모델 성능 비교 테스트
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.deepfake_detection import (
    CNNDeepfakeDetector,
    DeepFaceDetector,
    FaceRecognitionDetector,
    EnsembleDetector
)
import json
import time


def test_model(model, name, image_path):
    """단일 모델 테스트"""
    print(f"\n{'='*60}")
    print(f"모델: {name}")
    print(f"이미지: {image_path}")
    print(f"{'='*60}")
    
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        start_time = time.time()
        result = model.detect(image_bytes)
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ 탐지 완료 (소요 시간: {elapsed_time:.2f}초)")
        print(f"  - 판정: {'🚨 딥페이크' if result['is_fake'] else '✓ 진짜'}")
        print(f"  - 딥페이크 확률: {result['fake_probability']:.2%}")
        print(f"  - 신뢰도: {result['confidence']:.2%}")
        print(f"  - 의심 영역: {len(result['suspicious_regions'])}개")
        
        if 'analysis' in result:
            print(f"\n  분석 상세:")
            analysis = result['analysis']
            for key, value in analysis.items():
                if isinstance(value, dict):
                    print(f"    {key}:")
                    for k, v in value.items():
                        print(f"      - {k}: {v}")
                elif value is not None:
                    print(f"    - {key}: {value}")
        
        return {
            'success': True,
            'result': result,
            'time': elapsed_time
        }
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e),
            'time': 0
        }


def compare_models():
    """모든 모델 성능 비교"""
    print("\n" + "🎯 " * 20)
    print("딥페이크 탐지 모델 성능 비교 테스트")
    print("🎯 " * 20)
    
    # 테스트할 모델들
    models = [
        ("CNN Detector", CNNDeepfakeDetector()),
        ("DeepFace Detector", DeepFaceDetector()),
        ("Face Recognition Detector", FaceRecognitionDetector()),
        ("Ensemble Detector", EnsembleDetector())
    ]
    
    # 테스트 이미지들
    test_images = [
        ("images/original.jpeg", "원본 (진짜)"),
        ("images/deepfake.jpeg", "딥페이크 (가짜)"),
    ]
    
    # 생성된 이미지가 있으면 추가
    if os.path.exists("images/generated_deepfake.jpg"):
        test_images.append(("images/generated_deepfake.jpg", "생성된 딥페이크"))
    
    # 결과 저장
    all_results = {}
    
    # 각 이미지에 대해 모든 모델 테스트
    for image_path, image_desc in test_images:
        print(f"\n\n{'#'*70}")
        print(f"# 테스트 이미지: {image_desc}")
        print(f"{'#'*70}")
        
        image_results = {}
        
        for model_name, model in models:
            result = test_model(model, model_name, image_path)
            image_results[model_name] = result
        
        all_results[image_desc] = image_results
    
    # 종합 결과 출력
    print(f"\n\n{'='*70}")
    print("📊 종합 성능 비교")
    print(f"{'='*70}")
    
    for image_desc, results in all_results.items():
        print(f"\n{image_desc}:")
        print(f"{'-'*70}")
        print(f"{'모델명':<30} {'판정':<10} {'가짜확률':<12} {'시간(초)':<10}")
        print(f"{'-'*70}")
        
        for model_name, result in results.items():
            if result['success']:
                r = result['result']
                judgment = "딥페이크" if r['is_fake'] else "진짜"
                fake_prob = f"{r['fake_probability']:.2%}"
                elapsed = f"{result['time']:.2f}"
                print(f"{model_name:<30} {judgment:<10} {fake_prob:<12} {elapsed:<10}")
            else:
                print(f"{model_name:<30} {'실패':<10} {'-':<12} {'-':<10}")
    
    # 최고 성능 모델 추천
    print(f"\n\n{'='*70}")
    print("🏆 성능 평가 및 추천")
    print(f"{'='*70}")
    
    # 평균 처리 시간 계산
    avg_times = {}
    success_counts = {}
    
    for model_name, _ in models:
        times = []
        successes = 0
        for results in all_results.values():
            if results[model_name]['success']:
                times.append(results[model_name]['time'])
                successes += 1
        
        avg_times[model_name] = sum(times) / len(times) if times else float('inf')
        success_counts[model_name] = successes
    
    print("\n평균 처리 시간:")
    for model_name, avg_time in sorted(avg_times.items(), key=lambda x: x[1]):
        success_rate = success_counts[model_name] / len(test_images) * 100
        print(f"  {model_name}: {avg_time:.2f}초 (성공률: {success_rate:.0f}%)")
    
    # 추천
    fastest = min(avg_times.items(), key=lambda x: x[1])
    most_reliable = max(success_counts.items(), key=lambda x: x[1])
    
    print(f"\n🥇 가장 빠른 모델: {fastest[0]} ({fastest[1]:.2f}초)")
    print(f"🛡️  가장 안정적인 모델: {most_reliable[0]} (성공률: {most_reliable[1]}/{len(test_images)})")
    print(f"\n💡 추천: Ensemble Detector (여러 모델의 장점을 결합)")


if __name__ == "__main__":
    try:
        compare_models()
        
        print(f"\n\n{'='*70}")
        print("✓ 모든 테스트 완료")
        print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"\n❌ 치명적 에러: {str(e)}")
        import traceback
        traceback.print_exc()
