import os
import cv2
from django.shortcuts import render
from django.conf import settings
from ultralytics import YOLO

# YOLO 모델 (한 번만 로딩됨)
model = YOLO("yolov8n.pt")  # nano = 빠름

def upload_image(request):
    context = {}

    if request.method == "POST" and request.FILES.get("image"):
        img_file = request.FILES["image"]

        # 저장
        save_path = os.path.join(settings.MEDIA_ROOT, img_file.name)
        with open(save_path, "wb+") as f:
            for chunk in img_file.chunks():
                f.write(chunk)

        # YOLO 추론
        results = model(save_path)

        # 결과 이미지 생성
        img = cv2.imread(save_path)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = model.names[cls]

                cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(
                    img,
                    f"{label} {conf:.2f}",
                    (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )

        result_name = "result_" + img_file.name
        result_path = os.path.join(settings.MEDIA_ROOT, result_name)
        cv2.imwrite(result_path, img)

        context["result_img"] = settings.MEDIA_URL + result_name

    return render(request, "upload.html", context)
