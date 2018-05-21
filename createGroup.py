import init
import cognitive_face as CF

init.Init(CF)
try:
    CF.person_group.create(init.GROUP_ID, init.GROUP_NAME, init.GROUP_DATA)
except CF.util.CognitiveFaceException as e:
    if e.code == "PersonGroupExists":
        print("既にグループが存在しています")
else:
    print("グループが作成されました")