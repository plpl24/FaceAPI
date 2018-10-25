from faceCap_faceRecog.Recog.identify import identify_face
from faceCap_faceRecog.Recog import getFileFromSmb
from faceCap_faceRecog.spreedsheet import spSheets
import glob
import os
from datetime import datetime as dt
import shutil
import gspread


def dir_conf(dir_name: str):
    """
    ディレクトリが無ければ作成
    :param dir_name: ディレクトリの名前
    """
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)


class faceRecog_sort:
    def __init__(self, sorted_paths: list, sheet_name: str, faceapi_key: str):
        """
        :param sorted_paths: 識別する画像と振り分け先ディレクトリのパス　
                    0:顔が発見できなかった,1:個人を識別できた,2:個人を識別できなかった
        :param sheet_name: 識別した結果を書き込むspreadsheetsの名前
        :param identifyFace: 識別器
        """
        for path in sorted_paths:
            dir_conf(path)

        self.FaceNotMatch_path = sorted_paths[0]
        self.Identified_path = sorted_paths[1]
        self.FaceNotFound_path = sorted_paths[2]
        self.sheet_name = sheet_name
        self.face = identify_face(faceapi_key)

    def __call__(self, img_path, message: str, debug=False):
        """
        指定されたディレクトリ内の画像を識別して振り分けます
        :param img_path:  識別する画像が入っているフォルダ
        :param messagee spreadsheetに書き込むメッセージ
        :param debug: print文出力するかどうか
        """
        files = glob.glob("{}/*.jpg".format(img_path))

        if debug: print("顔認識開始")
        RESULT = []

        try:
            for file in files:
                file_name = os.path.basename(file)
                cap_time = dt.strptime(os.path.splitext(file_name)[0], getFileFromSmb.ft)  # 撮影した時間を取得

                try:
                    name = self.face.get_name(file, debug=debug)  # 顔識別
                    if name is None:  # 顔が識別できたか
                        shutil.move(file, "{}/{}".format(self.FaceNotMatch_path, file_name))
                    else:
                        shutil.move(file, "{}/{}".format(self.Identified_path,"{}_{}".format(name,file_name)))

                    RESULT.append({'time': cap_time, 'name': name})
                except ValueError:
                    if debug: print("顔が見つかりませんでした {}ファイルを{}に移動します".format(file_name, self.FaceNotFound_path))
                    shutil.move(file, "{}/{}".format(self.FaceNotFound_path, file_name))
        except KeyboardInterrupt as e:
            if debug: print("キーボード入力がありました,終了します")

        if debug: print('spreedSheetsに書込み開始')
        sheet = spSheets.sp_sheets(self.sheet_name)
        last_row = sheet.get_last_row('A')
        print("LAST＿LOW　＝　{}".format(last_row))
        for data in RESULT:
            last_row += 1
            sheet.write('A{}'.format(last_row), str(data['time']))
            sheet.write('B{}'.format(last_row), str(data['name']))
            sheet.write('C{}'.format(last_row), message)
        if debug: print(RESULT)


if __name__ == '__main__':
    IMG_path = 'IMG'  # smbから取得してきた画像が一時出来に保存される場所

    file_getter_entry = getFileFromSmb.getFileFromSmb('150.89.234.229',
                                                      'pi', 'raspberry', 'pi', 'images', IMG_path, debug=True,
                                                      isDelete=True)

    file_getter_exit = getFileFromSmb.getFileFromSmb('150.89.234.236',
                                                     'pi', 'raspberry', 'pi', 'images', IMG_path, debug=True,
                                                     isDelete=True)
    # file_getter_exit = getFileFromSmb.getFileFromSmb('', 'pi', 'Downloads\FaceAPI_old\\face', IMG_path)

    paths = ["faceNotMatch", "identifiedIMG", "faceNotFound"]
    recog = faceRecog_sort(paths, "faceRecog", "50a2cf7e80844d0c80b31c5d8ce16b96")

    while True :

        try:


            print("入室画像取得開始")

            file_getter_entry.get_images()
            recog(IMG_path, "入室しました", debug=True)

            print("退室画像取得開始")
            file_getter_exit.get_images()

            recog(IMG_path, "退室しました", debug=True)
            import time
            print("入退室処理完了一分後に再処理を開始します")
            time.sleep(60) #一分後に再識別
        except KeyboardInterrupt as e:
            exit(0)
