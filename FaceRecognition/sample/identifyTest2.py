import face_recognition
import cv2
import time

time0 = time.time()
hogeIMG = cv2.imread("known/hoge.jpg")
testIMG = cv2.imread("unknown/image1.jpg")


hogeIMG=cv2.resize(hogeIMG,None,fx=0.5,fy=0.5)
testIMG=cv2.resize(testIMG,None,fx=0.5,fy=0.5)

print("resize",time.time()-time0)
time0 = time.time()

faceLocations = face_recognition.face_locations(hogeIMG)

print("faceLocations1",time.time()-time0)
time0 = time.time()

hogeE = face_recognition.face_encodings(hogeIMG,faceLocations)

print("enc1",time.time()-time0)
time0 = time.time()

faceLocations = face_recognition.face_locations(testIMG)
# print(faceLocations) [(top, right, left, bottom), (46, 103, 89, 59)]


print("faceLocations2",time.time()-time0)
time0 = time.time()

testE = face_recognition.face_encodings(testIMG,faceLocations)  # 見つけた顔の数の特徴を表したリストが返ってくる
                                                  # 例えば二つの顔を見つけた場合　長さ2のリストを返す
print("enc2",time.time()-time0)
time0 = time.time()
for test in testE :
    res = face_recognition.compare_faces(hogeE, test)  # 第一引数は知っている顔のリスト
                                                           # 第二引数は調べたい顔の特徴点
    print(res) # 戻り値は第一引数の顔それぞれに対して一致するかどうかのリスト

print("print",time.time()-time0)