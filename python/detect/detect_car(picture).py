from ultralytics import YOLO
import cv2

# โหลดโมเดล YOLOv8
model = YOLO("yolov8n.pt")  # ใช้โมเดลสำเร็จรูป

# โหลดภาพที่ต้องการตรวจจับ
image_path = "car.jpg"  # เปลี่ยนเป็นรูปของคุณ
image = cv2.imread(image_path)

# ตรวจจับวัตถุในภาพ
results = model(image)

# แสดงผลลัพธ์
results[0].show()