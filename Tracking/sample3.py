import cv2
#コピー元
#http://ensekitt.hatenablog.com/entry/2017/12/21/200000
cascade_path = "haarcascade_frontalface_default.xml"

#顔認識を利用して顔を追跡
#顔を新しく認識したときには画像を保存する
def detectFace(cap):

    tracker = cv2.TrackerKCF_create()
    cascade = cv2.CascadeClassifier(cascade_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        facerect = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(1, 1),
                                                 maxSize=(1000, 1000))
        if len(facerect) > 0:
            print(facerect[0])

            ok = tracker.init(frame, tuple(facerect[0]))
            cv2.destroyAllWindows()
            break
        else:
            print("not found")

    print("newFaceDetected!!")
    import time
    import numpy
    cv2.imwrite("face Image {}.jpg".format(time.time()),numpy.array(frame))
    print("save image ",time.time())
    return tracker


if __name__ == '__main__':


    cap = cv2.VideoCapture(0)

    tracker = detectFace(cap)
    while True:
        # VideoCaptureから1フレーム読み込む
        ret, frame = cap.read()
        #frame = frame_resize(frame)
        if not ret:
            k = cv2.waitKey(1)
            if k == 27 :
                break
            continue

        # Start timer
        timer = cv2.getTickCount()

        # トラッカーをアップデートする
        track, bbox = tracker.update(frame)

        # FPSを計算する
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # 検出した場所に四角を書く
        if track:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)
        else :
            tracker = detectFace(cap)
            # トラッキングが外れたら警告を表示する
            cv2.putText(frame, "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);

        # FPSを表示する
        cv2.putText(frame, "FPS : " + str(int(fps)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);

        # 加工済の画像を表示する
        cv2.imshow("Tracking", frame)

        # キー入力を1ms待って、k が27（ESC）だったらBreakする
        k = cv2.waitKey(1)
        if k == 27 :
            break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()