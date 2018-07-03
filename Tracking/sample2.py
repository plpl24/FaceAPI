import cv2
#コピー元
#http://ensekitt.hatenablog.com/entry/2017/12/21/200000

#2つの物体を追跡するサンプル



if __name__ == '__main__':

    tracker = cv2.MultiTracker_create()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        #frame = frame_resize(frame)
        bbox = (0,0,10,10)
        bbox = cv2.selectROI(frame, False)
        print(bbox)
        ok = tracker.add(cv2.TrackerKCF_create(),frame, bbox)
        bbox = cv2.selectROI(frame, False)
        ok = tracker.add(cv2.TrackerKCF_create(),frame, bbox)
        cv2.destroyAllWindows()
        break

    while True:
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
        track, bbbox = tracker.update(frame)

        # FPSを計算する
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # 検出した場所に四角を書く
        if track:
            for bbox in bbbox:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)
        else :
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