#!/usr/bin/env python3
"""
InsightFace 모델 테스트
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.deepfake_detection import InsightFaceDetector
from models.deepfake_generation import InsightFaceGenerator
import time


def test_insightface_detector():
    """InsightFace 탐지 모델 테스트"""
    print("\n" + "="*70)
    print("🔍 InsightFace Detector 테스트")
    print("="*70)
    
    detector = InsightFaceDetector()
    
    test_images = [
        ("images/original.jpeg", "원본 (진짜)"),
        ("images/deepfake.jpeg", "딥페이크 (가짜)"),
    ]
    
    if os.path.exists("images/generated_deepfake.jpg"):
        test_images.append(("images/generated_deepfake.jpg", "생성된 딥페이크"))
    
    for image_path, desc in test_images:
        print(f"\n📸 테스트: {desc}")
        print(f"   이미지: {image_path}")
        
        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            
            start = time.time()
            result = detector.detect(image_bytes)
            elapsed = time.time() - start
            
            print(f"\n✅ 탐지 완료 (소요 시간: {elapsed:.2f}초)")
            print(f"   - 판정: {'🚨 딥페이크' if result['is_fake'] else '✓ 진짜'}")
            print(f"   - 가짜 확률: {result['fake_probability']:.2%}")
            print(f"   - 신뢰도: {result['confidence']:.2%}")
            print(f"   - 얼굴 탐지: {result['analysis'].get('faces_detected', 0)}개")
            
            if 'faces_info' in result['analysis']:
                for face_info in result['analysis']['faces_info']:
                    print(f"\n   얼굴 #{face_info['face_index'] + 1}:")
                    print(f"      - 탐지 신뢰도: {face_info.get('detection_confidence', 0):.2%}")
                    if 'age' in face_info:
                        print(f"      - 나이: {face_info['age']}세")
                    if 'gender' in face_info:
                        print(f"      - 성별: {face_info['gender']}")
                    if 'embedding_size' in face_info:
                        print(f"      - 임베딩 차원: {face_info['embedding_size']}D")
            
        except Exception as e:
            print(f"\n❌ 에러: {str(e)}")
            import traceback
            traceback.print_exc()


def test_insightface_generator():
    """InsightFace 생성 모델 테스트"""
    print("\n" + "="*70)
    print("🎨 InsightFace Generator 테스트")
    print("="*70)
    
    generator = InsightFaceGenerator()
    
    source_path = "images/original.jpeg"
    target_path = "images/deepfake.jpeg"
    output_path = "images/insightface_generated.jpg"
    
    print(f"\n📸 소스 이미지: {source_path}")
    print(f"📸 타겟 이미지: {target_path}")
    
    try:
        with open(source_path, "rb") as f:
            source_bytes = f.read()
        
        with open(target_path, "rb") as f:
            target_bytes = f.read()
        
        start = time.time()
        result = generator.generate(source_bytes, target_bytes)
        elapsed = time.time() - start
        
        if result['success']:
            print(f"\n✅ 생성 완료 (소요 시간: {elapsed:.2f}초)")
            print(f"   - 소스 얼굴: {result['source_faces']}개")
            print(f"   - 타겟 얼굴: {result['target_faces']}개")
            print(f"   - 스왑된 얼굴: {result['swapped_faces']}개")
            
            # 결과 저장
            with open(output_path, "wb") as f:
                f.write(result['image_bytes'])
            print(f"   - 저장 위치: {output_path}")
            
            # 분석 정보
            if 'analysis' in result:
                analysis = result['analysis']
                print(f"\n   📊 분석 정보:")
                
                if 'source_info' in analysis and analysis['source_info']:
                    src = analysis['source_info'][0]
                    print(f"      소스 얼굴:")
                    print(f"         - 탐지 신뢰도: {src.get('confidence', 0):.2%}")
                    if 'age' in src and src['age'] is not None:
                        print(f"         - 나이: {src['age']}세")
                    if 'gender' in src and src['gender'] is not None:
                        print(f"         - 성별: {src['gender']}")
                
                if 'target_info' in analysis and analysis['target_info']:
                    tgt = analysis['target_info'][0]
                    print(f"      타겟 얼굴:")
                    print(f"         - 탐지 신뢰도: {tgt.get('confidence', 0):.2%}")
                    if 'age' in tgt and tgt['age'] is not None:
                        print(f"         - 나이: {tgt['age']}세")
                    if 'gender' in tgt and tgt['gender'] is not None:
                        print(f"         - 성별: {tgt['gender']}")
        else:
            print(f"\n❌ 생성 실패: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ 에러: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n" + "🚀 " * 25)
    print("InsightFace 모델 종합 테스트")
    print("🚀 " * 25)
    
    try:
        # 탐지 테스트
        test_insightface_detector()
        
        # 생성 테스트
        test_insightface_generator()
        
        print("\n" + "="*70)
        print("✅ 모든 테스트 완료")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ 치명적 에러: {str(e)}")
        import traceback
        traceback.print_exc()
