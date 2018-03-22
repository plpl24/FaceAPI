import cognitive_face as CF
import cv2


#顔の座標情報からRect作成
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


#サブスクリプションキー
KEY=""

CF.Key.set(KEY)

#利用する地域のサーバーを指定
CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")

#画像パス
filePath = ""

#顔特定
faces = CF.face.detect(filePath)


#画像読み込み
image = cv2.imread(filePath)

for face in faces: #見つけた顔一つについて
    rect = getRectangle(face)
    cv2.rectangle(image,rect[0],rect[1],(255,255,255),3) #顔座標を書き込み


cv2.imshow("image",image) #画像表示
cv2.waitKey(0)