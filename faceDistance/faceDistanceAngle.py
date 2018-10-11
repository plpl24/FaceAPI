import cv2
import faceCap_faceRecog.Recog.identify
import numpy as np
import cv2
par = 130 # 実際と画像に映る顔の大きさの比率
wf = 17
is_rect_draw = True
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#idf = faceCap_faceRecog.Recog.identify.identify_face('50a2cf7e80844d0c80b31c5d8ce16b96')
cap = cv2.VideoCapture(0)
while True :
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.11, minNeighbors=5)
    if len(faces) != 0:
        x,y,w,h = faces[0]
        if is_rect_draw:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_color = frame[y:y+h, x:x+w]

        cv2.circle(frame,((int)(frame.shape[1]/2),(int)(frame.shape[0]/2)),5,(0,255,0),2)
        face_center_X = x + w / 2
        face_center_X = frame.shape[1]/2 - face_center_X #画像の中心と顔の距離X軸のみ
        pixel1 = wf/w #1ピクセルに対する現実の大きさ(センチメートル) 現実の顔の大きさと画像の大きさから計算
        facePos = pixel1*face_center_X*0.01 # 画像の中心と顔の距離 (メートル)
        distance = par / w
        print(facePos)
        angle = np.rad2deg(np.arcsin(facePos/distance))
        print("顔の距離は{}cm、角度は{}です".format(np.round(distance*100,2),angle))

    cv2.imshow('img',frame)
    if cv2.waitKey(1) == 113:
        cv2.destroyAllWindows()
        exit(0)



#frame = cv2.resize(frame, None, fx=0.5, fy=0.5)


#cv2.imwrite("hoge.jpg",frame)

#print(idf.get_name('hoge.jpg',debug=True))

