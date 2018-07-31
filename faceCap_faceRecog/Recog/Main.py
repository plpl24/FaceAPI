from faceCap_faceRecog.Recog.identify import IdentifyFace
from faceCap_faceRecog.Recog import getFileFromSmb
import glob
import os
from datetime import datetime as dt
import shutil


def dir_conf(target_dir):
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)


IMG_path = 'IMG' #smbから取得してきた画像が一時出来に保存される場所
dir_conf(IMG_path)
FaceNotFound_path = 'faceNotFound'
dir_conf(FaceNotFound_path)
Identified_path = 'identifiedIMG'
dir_conf(Identified_path)
FaceNotMatch_path = 'faceNotMatch'
dir_conf(FaceNotMatch_path)

wait_time = 60
idF = IdentifyFace("50a2cf7e80844d0c80b31c5d8ce16b96")
# x = getFileFromSmb.getFileFromSmb('150.89.234.237', 'pi', 'Downloads\FaceAPI_old\\face', IMG_path)


print("画像取得開始")
# x.get_images()
gl = glob.glob("{}/*.jpg".format(IMG_path))
print("顔認識開始")
RESULT = []

try:
    for file in gl:
        file_name = os.path.basename(file)
        create_time = dt.strptime(os.path.splitext(file_name)[0], getFileFromSmb.ft)
        try:
            name = idF.get_name(file)
            if name is None:
                shutil.move(file, "{}/{}".format(FaceNotMatch_path, file_name))
            else:
                shutil.move(file, "{}/{}".format(Identified_path, file_name))

            RESULT.append({'time': create_time.strftime(getFileFromSmb.ft), 'name': name})
        except ValueError:
            print("顔が見つかりませんでした {}\nファイルを{}に移動します".format(file_name, FaceNotFound_path))
            shutil.move(file, "{}/{}".format(FaceNotFound_path, file_name))
except KeyboardInterrupt as e:
    print("終了します")
print(RESULT)
exit(0)
