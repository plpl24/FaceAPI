import cv2
import cognitive_face as CF
from FaceAPI import init

camera = cv2.VideoCapture(1)
print(camera)

cascade_path = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(cascade_path)

init.Init(CF)

#全て配列で処理しているのでわかりずらい
# TODO 一つの顔について処理するよう変更
def detect(imgName):
    faces = CF.face.detect("face.jpg")  # 写真に写っている顔を複数個見つける

    if (len(faces) == 0):
        print("face API :: face not found")
        return None
    print("{}個のfaceを発見しました".format(len(faces)))

    faceRectArray = [f['faceRectangle'] for f in faces]

    facesArray = [f['faceId'] for f in faces]  # faceIDだけの配列に変換

    foundPerson = identify(facesArray)  # {'84c7f8c8-bc1d-4970-866f-8bd07b8a434f':
    # {'personId': 'bc858fd4-03b5-4619-a909-7f994afb8dbb', 'persistedFaceIds': ['3339eaff-ab67-4356-85cc-f8e54488d407',～～], 'name': 'Me', 'userData': 'info'}}


    return foundPerson


def identify(facesArray):
    try:
        response = CF.face.identify(facesArray, init.GROUP_ID)  # グループに似ている顔が存在しているか判定
    except CF.util.CogntiveFaceException as e:
        if e.code == "RateLimitExceeded":
            print("FaceAPI limit exceed")
    # -----顔に対応して最も一致率が高い人のdictを作成
    foundPerson = dict()  # 見つけた人の情報を入れるdictを作成
    for f in response:
        if len(f['candidates']) != 0:  # 候補者が存在したら
            personID = f['candidates'][0]['personId']  # 候補者のpersonIDを取得
            try:
                foundPerson[f['faceId']] = CF.person.get(init.GROUP_ID, personID)  # 見つけた人の情報を格納
            except CF.util.CogntiveFaceException as e:
                if e.code == "RateLimitExceeded":
                    print("FaceAPI limit exceed")
    return foundPerson


c, img = camera.read()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
facerect = cascade.detectMultiScale(gray, scaleFactor=1.11, minNeighbors=2, minSize=(10, 10), maxSize=(1000, 1000))
print(facerect)
if len(facerect) > 0:
    cv2.imwrite("face.jpg", img)
    print(detect("face.jpg"))

cv2.imshow("hoge", img)
cv2.waitKey(0)
