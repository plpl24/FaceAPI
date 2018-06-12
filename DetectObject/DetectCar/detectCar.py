import cv2


cas = 'carDitector.xml' #526枚の画像を学習させた分類器

image_path = 'car.jpg'

image =cv2.imread(image_path)
imageG = cv2.imread(image_path,0)

cascade = cv2.CascadeClassifier(cas)

rect = cascade.detectMultiScale(imageG,scaleFactor=1.1,
                                minNeighbors=2,minSize=(30,30))

color = (255,255,255)
print(rect)
if len(rect) > 0:

    #検出した顔を囲む矩形の作成
    for r in rect:
        cv2.rectangle(image, tuple(r[0:2]),tuple(r[0:2]+r[2:4]), color, thickness=2)


image = cv2.resize(image,None,fx=0.7,fy=0.7)
cv2.imshow("hogehoge",image)
cv2.waitKey(0)