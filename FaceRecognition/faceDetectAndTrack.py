import cv2
import face_recognition
import time
import numpy as np

scaleRate = 0.4  # カメラ画像の縮小率
maxFaceDistance = 30  # 前フレームの顔と現在の顔の最大距離、これを超えて顔が認識された場合別人として処理する
cameraID = 1
leftFrameCount = 5  # 顔が映らなくなってから、顔を保持するフレーム数
minFaceSize = 60  # 画像内に映る顔の最小の大きさ　小さくすると重くなる
index = 0
font = cv2.FONT_HERSHEY_DUPLEX


# 同時に最大で一人映っていると想定した下でのプログラム


class FacePos:
    def __init__(self, center_pos: np.array, face_name: str):
        self.__center = center_pos
        self.__faceName = face_name

    def update_on_same_face(self, center_pos: np.array):
        if maxFaceDistance > np.linalg.norm(self.__center - center_pos):
            self.__center = center_pos
            return True
        else:
            return False

    def get_face_name(self):
        return self.__faceName

    def get_center(self):
        return self.__center

class FaceProcessor:
    def __init__(self):
        self.cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.cascade.detectMultiScale(gray, scaleFactor=1.11, minNeighbors=2, minSize=(minFaceSize, minFaceSize))


class FaceDetectAndIdentify:
    def __init__(self):
        me_img = face_recognition.load_image_file("me.jpg")
        self.__me_face_enc = face_recognition.face_encodings(me_img)[0]

        self.camera = cv2.VideoCapture(cameraID)
        self.noFaceFrameCount = leftFrameCount

        self.face_processor = FaceProcessor()

    def __call__(self):
        timer = cv2.getTickCount()
        old_face = None
        while True:
            ret, frame = self.camera.read()
            frame = cv2.resize(frame, None, fx=scaleRate, fy=scaleRate)
            # locations = face_recognition.face_locations(frame) #face_recognitionを利用した場合の顔認識

            rect = self.face_processor.detect_face(frame)

            if len(rect) != 0:
                old_face = self.process_face(frame, rect,old_face)
            else:  # 顔が映っていなかった場合
                if old_face is not None:  # 過去に顔が映っていた場合
                    self.noFaceFrameCount = self.noFaceFrameCount - 1  # 残り保持フレーム数を減らす
                    if self.noFaceFrameCount <= 0:  # 保持フレーム数が無くなったら
                        print("oldFacePos delete", time.time())
                        old_face = None  # 過去の顔情報を消す

            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            timer = cv2.getTickCount()

            cv2.putText(frame, "FPS : " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                        cv2.LINE_AA)
            cv2.imshow("capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Release handle to the webcam
        self.camera.release()
        cv2.destroyAllWindows()

    def process_face(self, frame, rect, old_face):
        center = calc_center(rect[0])  # 中央座標計算

        if (old_face is not None) and old_face.update_on_same_face(
                np.array(center)):  # 過去の顔が存在し、過去の顔と近い場所に現在の顔が存在した場合 == 同じ顔が映り続けている場合
            self.noFaceFrameCount = leftFrameCount  # 残フレームリセット
        else:  # 新しい顔が認識された
            print("new person detected", time.time())
            old_face = self.create_new_face(center, frame)
            if old_face is None :
                return None
        cv2.circle(frame, center, 30, (255, 255, 0))  # 顔位置描画
        cv2.putText(frame, old_face.get_face_name(), (rect[0][0] + 6, rect[0][1] + rect[0][3] - 6), font, 0.6,
                    (255, 255, 255), 1)  # 名前描画
        return old_face


    def create_new_face(self, center, frame):
        name = self.get_name(frame)
        if name is None:  # cv2によって顔が認識されたがface_recognitionは顔を発見できなかった場合。次のフレームに進める
            return None
        return FacePos(center, self.get_name(frame))  # 新しく顔情報を生成

    # f : frame
    # return Name 顔を発見できなかった場合Noneを返します
    def get_name(self, f):
        face_encodings = face_recognition.face_encodings(f)
        if len(face_encodings) == 0:
            print("face_recognition :face not found")
            return None
        matches = face_recognition.compare_faces([self.__me_face_enc], face_encodings[0])

        global index
        index = index + 1
        return "{},{}".format(index, matches)


# array { x,y,width,height}
# return ( x ,y )
def calc_center(array):
    return (array[0] + int(array[2] / 2), array[1] + int(array[3] / 2))
    # return ((array[3] + int((array[1] - array[3]) / 2)), (array[0] + int((array[2] - array[0]) / 2)))


if __name__ == "__main__":
    f = FaceDetectAndIdentify()
    f()
