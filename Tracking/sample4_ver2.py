import cv2
import numpy as np
from datetime import datetime
import picamera
from picamera.array import PiRGBArray
import time
# コピー元
# http://ensekitt.hatenablog.com/entry/2017/12/21/200000

# 顔についてはKCFが安定
cascade_path = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(cascade_path)

def detect_face(f):
   
    
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    facerect = cascade.detectMultiScale(gray, scaleFactor=1.11, minNeighbors=2, minSize=(100, 100),)

    if len(facerect) != 0:
        return facerect
    else:
        return None


if __name__ == '__main__':

    # KCF
    tracker = []

   
    camera = picamera.PiCamera()
    camera.resolution = (640,480)
    camera.start_preview()
    camera.framerate = 30
    #camera.shutter_speed = 800
    time.sleep(2)
    image = np.empty((480 * 640 * 3,), dtype=np.uint8)
    timer = cv2.getTickCount()
    while True:
        localTimer = cv2.getTickCount()
        # VideoCaptureから1フレーム読み込む
        camera.capture(image, 'bgr',use_video_port = True)
        rawFrame = image.reshape((480, 640, 3))
       
        print("detectingTime =", (cv2.getTickCount() - localTimer) / cv2.getTickFrequency())
        # Start timer

        processFrame = np.copy(rawFrame)
        showFrame = np.copy(rawFrame)
        # トラッカーをアップデートする
        for tr in list(tracker):
            track, bbox = tr.update(rawFrame)
            if track:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(processFrame, p1, p2, (0, 255, 0), -1)
                cv2.rectangle(showFrame, p1, p2, (0, 255, 0), 2, 1)
            else:
                print("削除しました")
                tracker.remove(tr)


        rect = detect_face(processFrame)
        if rect is not None:
            tracker.append(cv2.TrackerKCF_create())
            tracker[-1].init(rawFrame, tuple(rect[0]))
            print("newFace {}.jpg".format(datetime.now().strftime("%m/%d %H:%M:%S")))
            cv2.imwrite("newFace {}.jpg".format(datetime.now().strftime("%m_%d %H_%M_%S")),rawFrame)
            print("tracker 追加,画像保存")

        # FPSを計算する
        fps = (cv2.getTickCount() - timer) /cv2.getTickFrequency()
        print(fps)
        
        timer = cv2.getTickCount()
        # FPSを表示する
        #cv2.putText(showFrame, "FPS : " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,cv2.LINE_AA)

        # 加工済の画像を表示する

        #cv2.imshow("rawFrame", rawFrame)
        #cv2.imshow("Tracking", showFrame)
        #cv2.imshow("processing", processFrame)

        # キー入力を1ms待って、k が27（ESC）だったらBreakする
        #k = cv2.waitKey(1)
        #if k == 27:
            #break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
