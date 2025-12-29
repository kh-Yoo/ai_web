import os
import cv2
from ultralytics import YOLO

# ===============================
# YOLO 모델 로드 (서버 시작 시 1회)
# ===============================
MODEL_PATH = "yolov8n.pt"   # 필요 시 yolov8s.pt, yolov8m.pt 가능

model = YOLO(MODEL_PATH)


def detect_image(image_path: str, save_path: str):
    """
    이미지 파일을 받아 YOLO 객체 탐지 수행 후
    바운딩 박스가 그려진 이미지를 저장한다.

    :param image_path: 업로드된 원본 이미지 경로
    :param save_path: 결과 이미지 저장 경로
    :return: 탐지 결과 리스트
    """

    # YOLO 추론 (CPU 사용)
    results = model(image_path)

    img = cv2.imread(image_path)
    detections = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]

            # 박스 그리기
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                img,
                f"{label} {conf:.2f}",
                (x1, max(y1 - 10, 0)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

            detections.append({
                "label": label,
                "confidence": round(conf, 3),
                "bbox": [x1, y1, x2, y2],
            })

    # 결과 이미지 저장
    cv2.imwrite(save_path, img)

    return detections
