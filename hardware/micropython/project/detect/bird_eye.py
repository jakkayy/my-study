import cv2
import numpy as np
from ultralytics import YOLO

# โหลดโมเดล YOLOv8 ที่ผ่านการ Train แล้ว
model = YOLO("yolov8n.pt")  # หรือaใช้ yolov8s.pt

# วิดีโอจากกล้อง
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# กำหนดจุด Perspective Transformation (ต้องปรับให้ตรงกับมุมกล้อง)
src_pts = np.float32([[200, 300], [400, 300], [50, 500], [550, 500]])  # จุดบนภาพจริง
dst_pts = np.float32([[100, 100], [300, 100], [100, 500], [300, 500]])  # จุดใน Bird's Eye View

# คำนวณ Matrix สำหรับแปลงมุมมอง
matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

# ความยาวจริงของพื้นถนนในภาพ (เมตร)
REAL_WORLD_WIDTH = 3.5  # สมมติว่าถนนกว้าง 3.5 เมตร
PIXEL_DISTANCE = np.linalg.norm(dst_pts[1] - dst_pts[0])  # คำนวณระยะห่างเป็นพิกเซล

# อัตราส่วนระยะจริงต่อตัวพิกเซล
PIXEL_TO_METER = REAL_WORLD_WIDTH / PIXEL_DISTANCE

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # แปลงมุมมองเป็น Bird’s Eye View
    bird_eye = cv2.warpPerspective(frame, matrix, (600, 600))

    # ใช้ YOLO ตรวจจับวัตถุ
    results = model(frame)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding Box
            class_id = int(box.cls[0])  # ประเภทของวัตถุ
            conf = box.conf[0]  # ความมั่นใจของโมเดล

            # ตรวจจับเฉพาะรถ (YOLO class_id 2 = car, 3 = motorcycle, 5 = bus, 7 = truck)
            if class_id in [2, 3, 5, 7] and conf > 0.5:
                # หา midpoint ของรถ
                mid_x = (x1 + x2) // 2
                mid_y = y2  # ใช้ขอบล่างของ Bounding Box เป็นจุดอ้างอิง

                # แปลงจุดไปยังมุมมอง Bird's Eye View
                transformed_point = cv2.perspectiveTransform(np.array([[[mid_x, mid_y]]], dtype="float32"), matrix)
                tx, ty = transformed_point[0][0]

                # คำนวณระยะจากตำแหน่งใน Bird’s Eye View
                distance = ty * PIXEL_TO_METER  # ระยะทางจากกล้อง

                # แสดง Bounding Box และระยะ
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{distance:.2f} m", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Bird's Eye View", bird_eye)

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
