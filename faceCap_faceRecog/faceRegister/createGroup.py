import cognitive_face as CF
import cv2
#グループ作成後、Person一人分を作成して顔写真(Face)を一枚分追加する


KEY="50a2cf7e80844d0c80b31c5d8ce16b96"

CF.Key.set(KEY)

# 利用する地域のサーバーを指定
CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")


GROUP_ID = "zemi_group"  # グループID グループにアクセスする際に必要になる 小英文字,数字,"-","_"のみ使用できる 最大長 64
GROUP_NAME = "zemiGroup"  # グループの名前 最大長128
GROUP_DATA = "zemi"  # グループに関するデータ　何でもいい　最大長16KB
if __name__ == '__main__':
    CF.person_group.delete(GROUP_ID)
    CF.person_group.create(GROUP_ID, GROUP_NAME, GROUP_DATA)  # グループ作成 グループID以外は指定しなくてもよい
# CF.person_group.get(groupID) #グループID,名前,ユーザーデータが取得できる



#CF.person_group.delete(GROUP_ID) #グループ削除 含まれているPerson,Face全て削除される
