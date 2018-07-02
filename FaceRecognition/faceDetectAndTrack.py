# coding:utf-8
import cv2
import face_recognition
import time
import numpy as np
from datetime import datetime

scaleRate = 0.4  # カメラ画像の縮小率
maxFaceDistance = 30  # 前フレームの顔と現在の顔の最大距離、これを超えて顔が認識された場合別人として処理する
cameraID = 1
leftFrameCount = 5  # 顔が映らなくなってから、顔を保持するフレーム数
minFaceSize = 60  # 画像内に映る顔の最小の大きさ　小さくすると重くなる
font = cv2.FONT_HERSHEY_DUPLEX
knownFaceDir = "knownFace"  # 知っている顔の写真(jpg)が入ったフォルダ　写真ファイル名がその人の名前として画面に表示される
logDir = "face_log"
unknownFaceDir = "unknownFace" # 知らない顔が検知されたときの画像を保存する場所
# 同時に最大で一人映っていると想定

# 顔の情報を扱うクラス
class FaceInfo:

    def __init__(self, center_pos: tuple, face_name: str):
        self.__center = np.array(center_pos)
        self.__faceName = face_name

    def update_on_same_face(self, center_pos: tuple):
        center_pos = np.array(center_pos)
        if maxFaceDistance > np.linalg.norm(self.__center - center_pos):
            self.__center = center_pos
            return True
        else:
            return False

    def get_face_name(self):
        return self.__faceName

    def get_center(self):
        return tuple(self.__center)


# 顔についての処理を行うクラス
class FaceProcessor:
    def __init__(self):
        import glob, os
        self.known_face_encodings = []  # 知っている顔の情報
        self.known_face_names = []  # 知っている顔の名前
        image_path = glob.glob("{}/*.jpg".format(knownFaceDir))
        for path in image_path:
            img = face_recognition.load_image_file(path)
            self.known_face_encodings.append(face_recognition.face_encodings(img)[0])  # 顔情報追加
            file_name = os.path.basename(path)
            file_name = file_name[:file_name.find(".")]
            self.known_face_names.append(file_name)  # ファイル名を追加
        self.cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rect = self.cascade.detectMultiScale(gray, scaleFactor=1.11, minNeighbors=2, minSize=(minFaceSize, minFaceSize))
        if len(rect) == 0:
            return None
        return rect[0][0] + int(rect[0][2] / 2), rect[0][1] + int(rect[0][3] / 2)  # 中央座標計算

    # 顔を識別して名前を返す
    # f : frame image
    # return face_recognitionが顔を発見できなかった場合Noneを返します
    def get_name(self, f):
        face_encodings = face_recognition.face_encodings(f)
        if len(face_encodings) == 0:
            print("face_recognition : face not found")
            return None

        matches = face_recognition.compare_faces(self.known_face_encodings, face_encodings[0])
        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_names[first_match_index]

        return name


class FaceDetectAndIdentify:
    def __init__(self):
        self.__face_processor = FaceProcessor()
        self.__old_face = None
        self.__no_face_frame_count = 0
        import os
        if not os.path.exists(logDir):
            os.mkdir(logDir)
        if not os.path.exists(unknownFaceDir):
            os.mkdir(unknownFaceDir)

    # 顔を検出、識別して見つけた顔(FaceInfo)を返す
    # frame : 画像フレーム
    def process(self, frame):
        frame = cv2.resize(frame, None, fx=scaleRate, fy=scaleRate)
        center = self.__face_processor.detect_face(frame)

        if center is not None:  # 顔が存在する
            if (self.__old_face is not None) and self.__old_face.update_on_same_face(
                    center):  # 過去の顔が存在し、過去の顔と近い場所に現在の顔が存在した場合 == 同じ顔が映り続けている場合
                self.__no_face_frame_count = leftFrameCount  # 残フレームリセット

            else:  # 新しい顔が認識された
                self.detect_new_face(center, frame)

        else:  # 顔が映っていなかった場合
            if self.__old_face is not None:  # 過去に顔が映っていた場合
                self.__no_face_frame_count = self.__no_face_frame_count - 1  # 残り保持フレーム数を減らす
                if self.__no_face_frame_count <= 0:  # 保持フレーム数が無くなったら
                    print("old face delete", time.time())
                    self.__old_face = None  # 過去の顔情報を消す

        return self.__old_face

    def detect_new_face(self, center, frame):
        print("new person detected", time.time())
        name = self.__face_processor.get_name(frame)
        if name is not None:
            print("{} detect".format(name))
            self.__old_face = FaceInfo(center, name)  # 新しく顔情報を生成
            if name is 'Unknown':
                cv2.imwrite("{}/unknownFace_{}.jpg".format(unknownFaceDir,datetime.now().strftime("%m/%d %H:%M:%S")), f)
            # log書き込み
            log = open("{}/face_log_{}.txt".format(logDir,datetime.now().strftime("%m_%d")), 'a+')
            log.write("{} detect \t {}\n".format(name, datetime.now().strftime("%y/%m/%d %H:%M:%S")))
            log.close()
        else:
            print("face_recognition not found face")  # cv2によって顔が認識されたがface_recognitionが顔を発見できなかった場合。


# メイン　主に描画処理を行う
if __name__ == "__main__":

    camera = cv2.VideoCapture(cameraID)
    f = FaceDetectAndIdentify()
    timer = cv2.getTickCount()

    while True:
        ret, frame = camera.read()
        face = f.process(frame)

        # ----draw to frame----------
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        timer = cv2.getTickCount()
        if face is not None:
            center = face.get_center()
            center = (int(x * (1 / scaleRate)) for x in center)
            center = tuple(center)
            cv2.circle(frame, center, 30, (255, 255, 0))  # 顔位置描画
            cv2.putText(frame, face.get_face_name(), (center[0] + 6, center[1] - 6), font, 0.6, (255, 255, 255),
                        1)  # 名前描画
        cv2.putText(frame, "FPS : " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                    cv2.LINE_AA)

        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    camera.release()
    cv2.destroyAllWindows()
