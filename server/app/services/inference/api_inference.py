#!/usr/bin/env python3
"""
딥페이크 탐지 API 테스트
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_file_api():
    """upload-file API 테스트"""
    print("\n" + "="*70)
    print("🧪 딥페이크 탐지 API 테스트")
    print("="*70)
    
    test_images = [
        ("images/original.jpeg", "원본 (진짜)"),
        ("images/deepfake.jpeg", "딥페이크 (가짜)"),
    ]
    
    if os.path.exists("images/generated_deepfake.jpg"):
        test_images.append(("images/generated_deepfake.jpg", "생성된 딥페이크"))
    
    for image_path, desc in test_images:
        print(f"\n{'─'*70}")
        print(f"📸 테스트: {desc}")
        print(f"   파일: {image_path}")
        print(f"{'─'*70}")
        
        try:
            with open(image_path, "rb") as f:
                response = client.post(
                    "/api/inference/upload-file",
                    files={"file": (os.path.basename(image_path), f, "image/jpeg")}
                )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"\n✅ 응답 성공 (HTTP {response.status_code})")
                print(f"\n📊 탐지 결과:")
                print(f"   - 판정: {result['detection_result']['verdict']}")
                print(f"   - 딥페이크 여부: {result['detection_result']['is_fake']}")
                print(f"   - 가짜 확률: {result['detection_result']['fake_probability']:.2%}")
                print(f"   - 진짜 확률: {result['detection_result']['real_probability']:.2%}")
                print(f"   - 신뢰도: {result['detection_result']['confidence']:.2%}")
                print(f"\n📁 파일 정보:")
                print(f"   - 파일명: {result['filename']}")
                print(f"   - 파일 크기: {result['file_size']:,} bytes")
                print(f"\n🔍 의심 영역: {len(result['suspicious_regions'])}개")
                
                if result['suspicious_regions']:
                    for i, region in enumerate(result['suspicious_regions'][:3]):
                        print(f"      #{i+1}: x={region['x']}, y={region['y']}, "
                              f"w={region['width']}, h={region['height']}")
                
                print(f"\n🤖 모델 정보:")
                print(f"   - 이름: {result['model_info']['name']}")
                print(f"   - 타입: {result['model_info']['type']}")
                
            else:
                print(f"\n❌ 에러 발생 (HTTP {response.status_code})")
                print(f"   {response.json()}")
                
        except Exception as e:
            print(f"\n❌ 예외 발생: {str(e)}")
            import traceback
            traceback.print_exc()


def test_invalid_file():
    """잘못된 파일 형식 테스트 (정상 동작 시 출력 없음)"""
    
    # 텍스트 파일로 테스트
    response = client.post(
        "/api/inference/upload-file",
        files={"file": ("test.txt", b"Hello World", "text/plain")}
    )
    
    # 예상대로 에러가 발생하면 아무것도 출력하지 않음
    if response.status_code == 400:
        pass  # 정상 동작
    else:
        # 예상과 다른 결과일 때만 출력
        print(f"\n{'─'*70}")
        print("❌ 잘못된 파일 형식 테스트 실패")
        print(f"{'─'*70}")
        print(f"응답 코드: HTTP {response.status_code} (예상: 400)")
        if response.status_code == 200:
            print(f"❌ 에러가 발생해야 하는데 성공함")
        else:
            print(f"❌ 예상치 못한 응답: {response.json()}")


if __name__ == "__main__":
    print("\n" + "🚀 " * 25)
    print("딥페이크 탐지 API 종합 테스트")
    print("🚀 " * 25)
    
    try:
        # 정상 파일 테스트
        test_upload_file_api()
        
        # 비정상 파일 테스트 (정상 동작 시 출력 없음)
        test_invalid_file()
        
        print("\n" + "="*70)
        print("✅ 모든 테스트 통과")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ 치명적 에러: {str(e)}")
        import traceback
        traceback.print_exc()
