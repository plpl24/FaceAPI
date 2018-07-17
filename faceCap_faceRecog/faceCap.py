import cv2
from datetime import datetime
camera = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("face_cascade.xml")
savePath = "."
while True :
    try:
        time0 = cv2.getTickCount()
        _,frame = camera.read()
        if frame is None:
            print("frame is None")
            exit()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faceRect = cascade.detectMultiScale(gray, scaleFactor=1.11, minNeighbors=2, minSize=(40, 40))
        if len(faceRect) != 0:
            cv2.imwrite("{}/faceCap_{}.jpg".format(savePath,datetime.now().strftime("%m_%d %H_%M_%S")),frame)
            print("detectFace")
        print("{}".format(cv2.getTickFrequency()/(cv2.getTickCount()-time0)))
    except KeyboardInterrupt as e:
        print("keyboard")
        exit()