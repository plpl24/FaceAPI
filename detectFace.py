# coding:utf-8
import io
import time
import threading
import picamera
import numpy as np
import cv2
import time
from datetime import datetime
import cognitive_face as CF
import init

init.Init(CF)
# Create a pool of image processors
done = False
lock = threading.Lock()
isSend = False
pool = []
color = (255, 255, 255)  # 白

cascade_path = "haarcascade_frontalface_default.xml"


class ImageProcessor(threading.Thread):
    def __init__(self, index):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()
        self.index = index
        self.cascade = cv2.CascadeClassifier(cascade_path)

    def printT(self, str):
        print("thread no = {} , {}".format(self.index, str))

    def identify(self, testIMG):
        faces = CF.face.detect(testIMG)  # 写真に写っている顔を複数個見つける

        if (len(faces) == 0):
            self.printT("face not found")
            return None

        self.printT("{}個のfaceを発見しました".format(len(faces)))

        facesArray = [f['faceId'] for f in faces]  # faceIDだけの配列に変換
        try:
            response = CF.face.identify(facesArray, init.GROUP_ID)  # グループに似ている顔が存在しているか判定
        except CF.util.CogntiveFaceException as e:
            if e.code == "RateLimitExceeded":
                self.printT("FaceAPI limit exceed")

        # -----顔に対応して最も一致率が高い人のdictを作成
        foundPerson = dict()  # 見つけた人の情報を入れるdictを作成
        for f in response:
            if len(f['candidates']) != 0:  # 候補者が存在したら
                personID = f['candidates'][0]['personId']  # 候補者のpersonIDを取得
                try:
                    foundPerson[f['faceId']] = CF.person.get(init.GROUP_ID, personID)  # 見つけた人の情報を格納
                except CF.util.CogntiveFaceException as e:
                    if e.code == "RateLimitExceeded":
                        self.printT("FaceAPI limit exceed")
        # --------写真への書き込み-----------------
        image = cv2.imread(testIMG)
        notFound = {'name': "Not found"}  # 似ている人が見つからなかった時用のdict

        return [foundPerson.get(face['faceId'], notFound)['name'] for face in faces]  # dict内に似ている人faceが存在したら名前を取得する

    def run(self):
        # This method runs in a separate thread
        global done, isSend
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    data = np.fromstring(self.stream.getvalue(), dtype=np.uint8)  # numpyの配列に変換
                    image = cv2.imdecode(data, 1)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    facerect = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(1, 1),
                                                             maxSize=(1000, 1000))

                    if len(facerect) > 0:

                        # 検出した顔を囲む矩形の作成
                        for rect in facerect:
                            dt = datetime.now()
                            self.printT("detect face {}.{}".format(dt.second, dt.microsecond))
                        cv2.imwrite("face{}.jpg".format(self.index), image)
                        if not isSend:
                            isSend = True
                            faces = self.identify("face{}.jpg".format(self.index))
                            if faces is not None:
                                self.printT(
                                    "face detected !! {}".format(self.identify("face{}.jpg".format(self.index))))
                                time.sleep(10)
                            else:
                                time.sleep(5)
                            isSend = False

                        else:
                            self.printT("FaceAPI is using")
                    else:
                        # self.printT("no face")
                        pass
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)


def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)


with picamera.PiCamera() as camera:
    pool = [ImageProcessor(i) for i in range(5)]
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.start_preview()
    time.sleep(2)
    camera.capture_sequence(streams(), use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
