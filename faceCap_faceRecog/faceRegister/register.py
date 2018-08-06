import glob
import sys
import cognitive_face as CF
from faceCap_faceRecog.faceRegister.createGroup import GROUP_ID

#顔画像を追加して学習させるプログラム
#personが見つからなかった場合は作成する

KEY = "50a2cf7e80844d0c80b31c5d8ce16b96"
CF.Key.set(KEY)
CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")

args = sys.argv
if len(args) != 3:
    print("引数が間違っています registerFace 名前　ディレクトリ")
    exit(1)

PERSON_NAME = args[1]  # 人の名前
PERSON_DATA = ""  # 人の情報


def getPersonID(PERSON_NAME):
    personList = CF.person.lists(GROUP_ID)
    for person in personList:
        if person['name'] == PERSON_NAME:
            return person['personId']
    return None


personID = getPersonID(PERSON_NAME)

if personID is None:
    res = CF.person.create(GROUP_ID, PERSON_NAME, PERSON_DATA)
    personID = res['personId']

print("名前　{} \nPersonID {}".format(PERSON_NAME,personID))
# -------顔写真登録開始-------------------
files = glob.glob("{}/*.jpg".format(args[2]))
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

print("learningComplete {}".format(CF.person.get(GROUP_ID,personID)))

# CF.person_group.delete(GROUP_ID)
