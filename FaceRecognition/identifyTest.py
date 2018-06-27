import face_recognition

hogeIMG = face_recognition.load_image_file("known/hoge.jpg")
testIMG = face_recognition.load_image_file("unknown/image1.jpg")

hogeE = face_recognition.face_encodings(hogeIMG)
testE = face_recognition.face_encodings(testIMG)  # 見つけた顔の数の特徴を表したリストが返ってくる
                                                  # 例えば二つの顔を見つけた場合　長さ2のリストを返す


for test in testE :
    res = face_recognition.compare_faces(hogeE, test)  # 第一引数は知っている顔のリスト
                                                           # 第二引数は調べたい顔の特徴点
    print(res) # 戻り値は第一引数の顔それぞれに対して一致するかどうかのリスト