# predict.py 실행 전에 이 코드로 이미지를 먼저 자르는 것을 추천합니다.
import dlib
import cv2
import numpy as np

def crop_face(image_path, save_path):
    detector = dlib.get_frontal_face_detector()
    img = cv2.imread(image_path)
    if img is None:
        print("이미지를 읽을 수 없습니다.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        print("❌ 얼굴을 찾지 못했습니다. 수동으로 잘라주세요.")
        return

    # 첫 번째 발견된 얼굴만 사용
    face = faces[0]
    
    # 여유 공간(Margin)을 조금 두고 자르기 (DeepfakeBench 스타일)
    x1, y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()
    
    # 마진 추가 (약 30% 정도 더 넓게 잡는 것이 일반적)
    w, h = x2 - x1, y2 - y1
    margin = int(w * 0.2) 
    
    x1 = max(0, x1 - margin)
    y1 = max(0, y1 - margin)
    x2 = min(img.shape[1], x2 + margin)
    y2 = min(img.shape[0], y2 + margin)

    cropped_img = img[y1:y2, x1:x2]
    cv2.imwrite(save_path, cropped_img)
    print(f"✅ 얼굴을 잘라서 저장했습니다: {save_path}")

# 사용 예시
crop_face("C:/Users/USER/Downloads/DeepfakeBench-main/DeepfakeBench-main/face/cropped_test2.png", "cropped_test2.png")