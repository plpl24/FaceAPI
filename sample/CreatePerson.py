import cognitive_face as CF
import cv2

KEY=""

CF.Key.set(KEY)

# 利用する地域のサーバーを指定
CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")


groupID = "test_group"  # グループID グループにアクセスする際に必要になる 小英文字,数字,"-","_"のみ使用できる 最大長 64
name = "test_name"  # グループの名前 最大長128
user_data = "test_data"  # グループに関するデータ　何でもいい　最大長16KB


CF.person_group.create(groupID,name,user_data)  # グループ作成 グループID以外は指定しなくてもよい
# CF.person_group.get(groupID) #グループID,名前,ユーザーデータが取得できる


response = CF.person.create(groupID, "person_name", "person_data") # パーソン作成　グループID以外は指定しなくてもよい　戻り値はpersonIdを含むdictionary
personID = response["personId"] # personID取り出し
# CF.person.lists(groupID) #グループに含まれるPersonのPersonID,Face,name,userDataのリストを返す

# 画像パス
filePath = ""

res = CF.person.add_face(filePath,groupID,personID,"face_data")  # Personに顔の画像追加 引数のface_dataについては省略可能
                                                                  # 渡す画像に二つ以上顔が含まれている場合は,5つめの引数で追加対象の顔を指定しなければならない
                                                                  # 戻り値は、渡した画像の顔を表すFaceIDを含むdictionary

#  CF.person.get(groupID,personID)  #Personに含まれるpersonId,登録されたFaceIdのリスト,name,user_dataを返す

print(CF.person.get(groupID,personID))


CF.person_group.delete(groupID) #グループ削除 含まれているPerson,Face全て削除される
