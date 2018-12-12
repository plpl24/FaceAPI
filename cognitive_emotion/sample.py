# identify_emotionの使い方
from cognitive_emotion.identify_emotion import emotion_face
e = emotion_face("50a2cf7e80844d0c80b31c5d8ce16b96")
print(e.detect_emotion("face.jpg"))