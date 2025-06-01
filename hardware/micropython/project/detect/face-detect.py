import cv2 as cv


img = cv.imread("C:/hardware/micropython/project/human.jpeg")
face_model = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
gray_scale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
faces = face_model.detectMultiScale(gray_scale)

for (x,y,z,h) in faces:
    cv.rectangle(img, (x,y), (x+z,y+h), (255,255,255), 2)
    


cv.imshow("image", img)
cv.waitKey(0)
cv.destroyAllWindows()
