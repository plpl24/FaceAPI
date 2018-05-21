import cognitive_face as CF
import init
import time

init.Init(CF)

# -----学習開始-------------
try:
    #print("{}人のpersonが登録されています".format(len(CF.person.lists(init.GROUP_ID))))
    CF.person_group.train(init.GROUP_ID)
except CF.util.CognitiveFaceException as e:
    if e.code == "PersonGroupNotFound":
        print("グループが作成されていません、先にcreateGroup.pyとcreatePersonを実行して下さい")
        print(e)
        exit(1)

print("学習開始しました")

time.sleep(1)
# -----学習終了待ち ---------
result = CF.person_group.get_status(init.GROUP_ID)
while result ["status"] == "running":

    print("waiting....")
    time.sleep(1)
    result = CF.person_group.get_status(init.GROUP_ID)

print("学習完了しました 開始時間={} , 終了時間 ={}".format(result["createdDateTime"],result["lastActionDateTime"]))
