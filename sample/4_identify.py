import cognitive_face as CF
import cv2
import glob


# 必ず learningFaceを実行した後に実行する
# sample/test内の写真にlearningFaceで学習した人が映っているかどうかを表示する
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


KEY = ""

CF.Key.set(KEY)

CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")

GROUP_ID = "test_group"  # グループID グループにアクセスする際に必要になる 小英文字,数字,"-","_"のみ使用できる 最大長 64
GROUP_NAME = "test_name"  # グループの名前 最大長128
GROUP_DATA = "test_data"  # グループに関するデータ　何でもいい　最大長16KB

PERSON_NAME = "person_name"  # 人の名前
PERSON_DATA = "person_data"  # 人の情報

files = glob.glob('test/*.jpg')

for testIMG in files:  # test内の写真について

    faces = CF.face.detect(testIMG)  # 写真に写っている顔を複数個見つける

    if (len(faces) == 0):
        print("face not found")
        continue

    print("{}個のfaceを発見しました".format(len(faces)))

    facesArray = [f['faceId'] for f in faces]  # faceIDだけの配列に変換
    response = CF.face.identify(facesArray, GROUP_ID)  # グループに似ている顔が存在しているか判定

    # -----顔に対応して最も一致率が高い人のdictを作成
    foundPerson = dict()  # 見つけた人の情報を入れるdictを作成
    for f in response:
        if len(f['candidates']) != 0:  # 候補者が存在したら
            personID = f['candidates'][0]['personId']  # 候補者のpersonIDを取得
            foundPerson[f['faceId']] = CF.person.get(GROUP_ID, personID)  # 見つけた人の情報を格納

    # --------写真への書き込み-----------------
    image = cv2.imread(testIMG)
    for face in faces:  # 見つけた顔一つについて

        # -----detectFaceと同じ-----
        rect = getRectangle(face)
        cv2.rectangle(image, rect[0], rect[1], (255, 255, 255), 3)  # 顔座標を書き込み
        # -------
        notFound = {'name':"Not found"} #似ている人が見つからなかった時用のdict
        name = foundPerson.get(face['faceId'], notFound)['name'] #dict内に似ている人faceが存在したら名前を取得する
        cv2.putText(image, name, (rect[0][0], rect[1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 2, cv2.LINE_AA)                     # 画像に書き込み


    cv2.imshow(testIMG, image)  # 画像表示

cv2.waitKey(0)
