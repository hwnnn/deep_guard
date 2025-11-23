#!/usr/bin/env python3
"""
딥페이크 탐지 및 생성 테스트 스크립트
"""
import sys
import os

# 프로젝트 루트를 PYTHONPATH에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.deepfake_detection import CNNDeepfakeDetector
from models.deepfake_generation import SimpleFaceSwapGenerator
import json


def test_deepfake_detection():
    print("=" * 60)
    print("딥페이크 탐지 테스트")
    print("=" * 60)
    
    detector = CNNDeepfakeDetector()
    
    # 원본 이미지 테스트
    print("\n[1] 원본 이미지 분석 (original.jpeg)")
    with open("images/original.jpeg", "rb") as f:
        original_bytes = f.read()
    
    result_original = detector.detect(original_bytes)
    print(json.dumps(result_original, indent=2, ensure_ascii=False))
    
    # 딥페이크 이미지 테스트
    print("\n[2] 딥페이크 이미지 분석 (deepfake.jpeg)")
    with open("images/deepfake.jpeg", "rb") as f:
        deepfake_bytes = f.read()
    
    result_deepfake = detector.detect(deepfake_bytes)
    print(json.dumps(result_deepfake, indent=2, ensure_ascii=False))
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("결과 요약")
    print("=" * 60)
    print(f"원본 이미지:")
    print(f"  - 판정: {'딥페이크' if result_original['is_fake'] else '진짜'}")
    print(f"  - 딥페이크 확률: {result_original['fake_probability']:.2%}")
    print(f"  - 진짜 확률: {result_original['real_probability']:.2%}")
    print(f"  - 의심 영역 개수: {len(result_original['suspicious_regions'])}")
    
    print(f"\n딥페이크 이미지:")
    print(f"  - 판정: {'딥페이크' if result_deepfake['is_fake'] else '진짜'}")
    print(f"  - 딥페이크 확률: {result_deepfake['fake_probability']:.2%}")
    print(f"  - 진짜 확률: {result_deepfake['real_probability']:.2%}")
    print(f"  - 의심 영역 개수: {len(result_deepfake['suspicious_regions'])}")


def test_deepfake_generation():
    print("\n" + "=" * 60)
    print("딥페이크 생성 테스트")
    print("=" * 60)
    
    generator = SimpleFaceSwapGenerator()
    
    print("\n[3] 딥페이크 생성 (original.jpeg → deepfake.jpeg 기반)")
    
    with open("images/original.jpeg", "rb") as f:
        source_bytes = f.read()
    
    with open("images/deepfake.jpeg", "rb") as f:
        target_bytes = f.read()
    
    try:
        result_bytes = generator.generate(source_bytes, target_bytes)
        
        # 결과 저장
        output_path = "images/generated_deepfake.jpg"
        with open(output_path, "wb") as f:
            f.write(result_bytes)
        
        print(f"✓ 딥페이크 생성 성공!")
        print(f"  - 저장 경로: {output_path}")
        print(f"  - 파일 크기: {len(result_bytes)} bytes")
        
        # 생성된 이미지 탐지
        print("\n[4] 생성된 딥페이크 검증")
        detector = CNNDeepfakeDetector()
        detection_result = detector.detect(result_bytes)
        
        print(f"  - 판정: {'딥페이크' if detection_result['is_fake'] else '진짜'}")
        print(f"  - 딥페이크 확률: {detection_result['fake_probability']:.2%}")
        print(f"  - 의심 영역: {len(detection_result['suspicious_regions'])}개")
        
    except Exception as e:
        print(f"✗ 딥페이크 생성 실패: {str(e)}")


def main():
    print("\n" + "🔍 " * 20)
    print("Deep Guard - 딥페이크 탐지 및 생성 테스트")
    print("🔍 " * 20 + "\n")
    
    try:
        # 1. 딥페이크 탐지 테스트
        test_deepfake_detection()
        
        # 2. 딥페이크 생성 테스트
        test_deepfake_generation()
        
        print("\n" + "=" * 60)
        print("✓ 모든 테스트 완료")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
