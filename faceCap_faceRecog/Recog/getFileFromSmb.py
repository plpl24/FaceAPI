from smb.SMBConnection import SMBConnection
import platform
import io
import cv2
import numpy as np
import os
from datetime import datetime as dt

# とってきた画像の名前は　作成日時.jpgになる
# 作成日時:YYYY_MM_dd_HH_mm_ss_ms

ft = '%Y_%m_%d_%H_%M_%S_%f'


# 指定されたディレクトリ内の画像をローカルにコピーする
# get_imagesを呼び出すたびに、画像が作成された日時を確認して、新たに作成された画像のみがコピーされる
class getFileFromSmb:
    def __init__(self, ip_address, id, pw, service_name, retrieve_path, save_path, max_IMG=10, debug=False):
        self.dataFile_name = 'last_time.txt'
        self.__conn = SMBConnection(
            id,  # ID
            pw,  # PW
            platform.uname().node,
            '',
        )
        if not self.__conn.connect(ip_address):
            raise ValueError("smbサーバに接続できません")

        self.__service_name = service_name
        self.__retrieve_path = retrieve_path
        self.__save_path = save_path
        self.__debug = debug
        self.__last_time = dt.min

        if os.path.isfile(self.dataFile_name):
            with open(self.dataFile_name, 'r+') as file:
                data = file.read()
                self.__last_time = dt.strptime(data, ft)

        if self.__debug:
            print('getFileFromSmb初期化　最終更新日時は{}に設定されました.'.format(self.__last_time))

    def get_images(self):
        file_list = self.__conn.listPath(self.__service_name, self.__retrieve_path)
        if len(file_list) == 0:
            raise ValueError("files not found")

        last_time_tmp = self.__last_time  # 一時的に最新の画像日時を保存する
        copy_count = 0
        for file in file_list:
            file_name = file.filename
            if os.path.splitext(file_name)[1] != '.jpg' and os.path.splitext(file_name)[1] != '.png':
                continue  # 画像ではない

            create_time = self.__get_create_time(file_name)  # 画像作成日時
            if self.__last_time < create_time:
                if self.__debug:
                    print("{}をコピーします".format(file_name))
                copy_count = copy_count + 1
                self.__retrieve_image(file_name, create_time)  # 画像保存

                if last_time_tmp < create_time:
                    last_time_tmp = create_time  # 最新画像作成日時を保存
        self.__last_time = last_time_tmp  # 実際に更新
        if self.__debug:
            print("最終更新日時を更新しました {}".format(self.__last_time))
        with open(self.dataFile_name, 'w+') as file:
            file.write(self.__last_time.strftime(ft))
        if self.__debug:
            print("{}枚をコピーしました".format(copy_count))

    def __get_create_time(self, file_name):
        return dt.fromtimestamp(
            self.__conn.getAttributes(self.__service_name, '{}\{}'.format(self.__retrieve_path, file_name)).create_time)

    def __retrieve_image(self, file_name, create_time):
        new_name = "{}.jpg".format(create_time.strftime(ft))
        with open('{}\{}'.format(self.__save_path, new_name), 'wb') as file:
            self.__conn.retrieveFile(self.__service_name, '{}\{}'.format(self.__retrieve_path, file_name), file)
