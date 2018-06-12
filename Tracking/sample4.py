import cv2
import numpy as np
from datetime import datetime
# コピー元
# http://ensekitt.hatenablog.com/entry/2017/12/21/200000

# 顔についてはKCFが安定
cascade_path = "haarcascade_frontalface_default.xml"


def detect_face(f):
    cascade = cv2.CascadeClassifier(cascade_path)

    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    facerect = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(1, 1),
                                        maxSize=(1000, 1000))
    if len(facerect) != 0:
        return facerect
    else:
        return None


if __name__ == '__main__':

    # KCF
    tracker = []

    # TLD #GPUコンパイラのエラーが出ているっぽい
    # tracker = cv2.TrackerTLD_create()

    # MedianFlow
    # tracker = cv2.TrackerMedianFlow_create()

    # GOTURN # モデルが無いよって怒られた
    # https://github.com/opencv/opencv_contrib/issues/941#issuecomment-343384500
    # https://github.com/Auron-X/GOTURN-Example
    # http://cs.stanford.edu/people/davheld/public/GOTURN/trained_model/tracker.caffemodel
    # tracker = cv2.TrackerGOTURN_create()

    cap = cv2.VideoCapture(0)



    while True:
        # VideoCaptureから1フレーム読み込む
        ret, rawFrame = cap.read()

        # frame = frame_resize(frame)
        if not ret:
            k = cv2.waitKey(1)
            if k == 27:
                break
            continue

        # Start timer
        timer = cv2.getTickCount()

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
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # FPSを表示する
        cv2.putText(showFrame, "FPS : " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                    cv2.LINE_AA)

        # 加工済の画像を表示する

        #cv2.imshow("rawFrame", rawFrame)
        cv2.imshow("Tracking", showFrame)
        #cv2.imshow("processing", processFrame)

        # キー入力を1ms待って、k が27（ESC）だったらBreakする
        k = cv2.waitKey(1)
        if k == 27:
            break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
