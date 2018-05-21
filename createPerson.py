import glob
import sys

import cognitive_face as CF

import init

# personを作成し、顔写真を登録します
# python createPerson.py 名前 情報 顔写真が格納されたフォルダ(jpg)
init.Init(CF)

args = sys.argv
if len(args) != 4:
    print("引数が正しくありません")
    print("createPerson.py 名前 情報 顔写真が格納されたフォルダ(jpg)")
    exit(1)

PERSON_NAME = args[1]  # 人の名前
PERSON_DATA = args[2]  # 人の情報
imgDir = args[3]

images = glob.glob("{}/*.jpg".format(imgDir))

if len(images) < 1:
    print("画像が見つかりませんでした")
print("画像が{}枚見つかりました".format(len(images)))
try:
    response = CF.person.create(init.GROUP_ID, PERSON_NAME, PERSON_DATA)
except CF.util.CognitiveFaceException as e:
    if e.code == "PersonGroupNotFound":
        print("グループが作成されていません、先にcreateGroup.pyを実行して下さい")
        print(e)
        exit(1)

personID = response["personId"]
print("personを作成しました personId = {}".format(personID))

print("顔写真登録を始めます")
# -------顔写真登録開始------------------

count = 0
for file in images:
    print("---------{}登録開始----------".format(file))
    try:
        res = CF.person.add_face(file, init.GROUP_ID, personID, "file={}".format(file))
    except CF.util.CognitiveFaceException as e:
        print("エラーが発生しました\n {}".format(e))
    else:
        print("顔写真が登録されました faceID={}".format(res["persistedFaceId"]))
        count += 1

print("-----------------------\n{}枚の顔写真が登録されました".format(count))
