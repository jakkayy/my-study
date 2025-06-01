from ultralytics import YOLO
import cv2 as cv
import time

model = YOLO("yolov8n.pt")

cap = cv.VideoCapture(1, cv.CAP_DSHOW)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    result = model(frame)
    annotated = result[0].plot()
    cv.imshow("YOLO_Capture", annotated)
    
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.5)

cap.release()
cv.destroyAllWindows()