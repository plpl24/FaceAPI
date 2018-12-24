import cognitive_face as CF
import cv2

# 出力結果　[{'faceId': 'aa2fa9b3-86fa-4f06-94c1-ff93e913e0ae', 'faceRectangle': {'top': 153, 'left': 61, 'width': 137, 'height': 137}}]

#顔の座標情報からRect作成
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


#サブスクリプションキー
KEY="50a2cf7e80844d0c80b31c5d8ce16b96"

CF.Key.set(KEY)

#利用する地域のサーバーを指定
CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")

#画像パス
filePath = "face1.jpg"

#顔特定
faces = CF.face.detect(filePath)

print(faces)
#画像読み込み
image = cv2.imread(filePath)

for face in faces: #見つけた顔一つについて
    rect = getRectangle(face)
    cv2.rectangle(image,rect[0],rect[1],(255,255,255),3) #顔座標を書き込み


cv2.imshow("image",image) #画像表示
cv2.waitKey(0)