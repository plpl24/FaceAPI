class emotion_face:
    def __init__(self, KEY):
        import cognitive_face as CF
        self.CF = CF
        self.CF.Key.set(KEY)

        # 利用する地域のサーバーを指定
        self.CF.BaseUrl.set("https://eastasia.api.cognitive.microsoft.com/face/v1.0")


    # img_path:画像パス
    # 戻り値:感情とその感情である確率
    def detect_emotion(self, img_path):
        # 顔特定
        faces = self.CF.face.detect(img_path, attributes='emotion')

        if len(faces) > 1:
            raise ValueError("顔が複数検出されました")

        face = faces[0]
        emotion = face['faceAttributes']['emotion']
        # 戻り値サンプル：{'anger': 0.0, 'contempt': 0.002, 'disgust': 0.0, 'fear': 0.0,
        #                  'happiness': 0.786, 'neutral': 0.212, 'sadness': 0.0, 'surprise': 0.0}

        values = list(emotion.values())
        top_index = values.index(max(values))
        return list(emotion.keys())[top_index],values[top_index]


