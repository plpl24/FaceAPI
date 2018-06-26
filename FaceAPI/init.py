
GROUP_ID = "oit_id"  # グループID グループにアクセスする際に必要になる 小英文字,数字,"-","_"のみ使用できる 最大長 64
GROUP_NAME = "OIT_GROUP"  # グループの名前 最大長128
GROUP_DATA = ""  # グループに関するデータ　何でもいい　最大長16KB
KEY = "50a2cf7e80844d0c80b31c5d8ce16b96"
from urllib3.exceptions import InsecureRequestWarning
import urllib3

class Init:
    def __init__(self,CF):
        urllib3.disable_warnings(InsecureRequestWarning)
        CF.Key.set(KEY)
        CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")
