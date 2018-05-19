import cognitive_face as CF
KEY = ""

CF.Key.set(KEY)

# 利用する地域のサーバーを指定
CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")

GROUP_ID = "test_group"

CF.person_group.delete(GROUP_ID)