from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator, colors
import cv2 as cv

model = YOLO("yolovBn.pt")

def draw_box(frame, boxes):
    annotator = Annotator(frame)
    for box in boxes:
        class_id = box.cls
        class_name = model.names[int(class_id)]
        coordinator = box.xyxy[0]
        confidence = box.conf
        
        annotator.box_lable(box=coordinator, lable=class_name, color=colors)
    return annotator.result()
        
def detct_motorcycle(frame):
    """detect motorcycle from input image"""
    consider_classes = [0,3]
    confidence_threshold = 0.5
    results = model.predict(frame, conf=confidence_threshold , classes=consider_classes)
    
    for result in results:
         frame = draw_box(frame, result.boxes)
    return frame
if __name__ == "__main__":
    
    video.path = "video.mov"
    cap = cv.VideoCapture(video.path)
    
    while cap.is0pened():
        ret, frame = cap.read()
        if ret:
            cv.imshow("frame", frame)
            cv.waitKey(1)
        else:
            break
        
        cap.release()
        cv.destroyAllWindows()