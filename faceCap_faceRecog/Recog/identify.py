import cognitive_face as CF
from time import sleep


class identify_face:
    def __init__(self, key, group_id="zemi_group", wait_time=60, ):
        KEY = key
        self.wait_time = wait_time
        CF.Key.set(KEY)
        CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")
        CF.person_group.train(group_id)
        print(CF.person_group.get_status(group_id)["status"])
        self.__GROUP_ID = group_id  # グループID グループにアクセスする際に必要になる 小英文字,数字,"-","_"のみ使用できる 最大長 64

    # 画像に映っている人の名前を返す
    # 顔が映っていなかった場合　ValueError
    # 候補者が見つからなかった場合 None
    def get_name(self, img_path, debug=False):
        try:
            faces = CF.face.detect(img_path)  # 写真に写っている顔を複数個見つける

            if len(faces) != 1:
                raise ValueError("顔が見つからなかったか、複数の顔が発見されました")

            face_array = [f['faceId'] for f in faces]  # faceIDだけの配列に変換
            response = CF.face.identify(face_array, self.__GROUP_ID)  # グループに似ている顔が存在しているか判定

            response = response[0]  # 一人目のみ取得
            if len(response['candidates']) != 0:  # 候補者が存在したら
                person_id = response['candidates'][0]['personId']  # 候補者のpersonIDを取得
                return CF.person.get(self.__GROUP_ID, person_id)['name']
            else:
                return None
        except CF.util.CognitiveFaceException as e:
            if debug:
                if e.status_code == 403:
                    print("faceAPI使用上限を超えました {}秒後に再識別を開始します".format(self.wait_time))
                    for i in range(self.wait_time):
                        sleep(1)
                        if debug:
                            print(self.wait_time - i)
                else:
                    print(e)
                    exit(1)
            return self.get_name(img_path)
