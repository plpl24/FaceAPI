import init
import cognitive_face as CF

init.Init(CF)
try:
    CF.person_group.delete(init.GROUP_ID)
except CF.util.CognitiveFaceException as e:
    if e.code == "PersonGroupNotFound":
        print("グループが存在していません")
else:
    print("グループが削除されました")