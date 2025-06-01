import cv2 as cv
import requests

NODE_RED_URL = "http://localhost:1880/upload"

cap = cv.VideoCapture(0, cv.CAP_DSHOW)  # เปิดกล้อง

while True:
    ret, frame = cap.read()
    if not ret:
        break

    _, img_encoded = cv.imencode(".jpg", frame)
    files = {"file": ("image.jpg", img_encoded.tobytes(), "image/jpeg")}

    try:
        response = requests.post(NODE_RED_URL, files=files)
        print(response.text)
    except Exception as e:
        print("❌ ส่งภาพไม่สำเร็จ:", e)

    cv.imshow("Webcam", frame)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv.destroyAllWindows()