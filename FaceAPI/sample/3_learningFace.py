import glob

import cognitive_face as CF

#sample/facesに入っている顔写真を人として登録する
#学習結果を削除したい場合はdeleteGroupを実行

KEY = ""

CF.Key.set(KEY)

# 利用する地域のサーバーを指定
CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")

# --- グループ,Person作成 ---------


GROUP_ID = "test_group"  # グループID グループにアクセスする際に必要になる 小英文字,数字,"-","_"のみ使用できる 最大長 64
GROUP_NAME = "test_name"  # グループの名前 最大長128
GROUP_DATA = "test_data"  # グループに関するデータ　何でもいい　最大長16KB

PERSON_NAME = "person_name"  # 人の名前
PERSON_DATA = "person_data"  # 人の情報
CF.person_group.create(GROUP_ID, GROUP_NAME, GROUP_DATA)
response = CF.person.create(GROUP_ID, PERSON_NAME, PERSON_DATA)
personID = response["personId"]

# -------顔写真登録開始-------------------
files = glob.glob('faces/*.jpg')

index = 0
for file in files:
    print("{} 写真登録".format(file))
    res = CF.person.add_face(file, GROUP_ID, personID, "face_data {}".format(index))
    index += 1
    # --
    # if (index > 2): break

# -----学習開始-------------

CF.person_group.train(GROUP_ID)

# -----学習終了待ち ---------
while CF.person_group.get_status(GROUP_ID)["status"] == "running":
    import time

    print("waiting....")
    time.sleep(1)

print("learningComplete")

# CF.person_group.delete(GROUP_ID)
