from smb.SMBConnection import SMBConnection
import platform
import io
import cv2
import numpy as np
import os
if __name__ == "__main__":

    # connection open
    conn = SMBConnection(
        'pi',
        'raspberry',
        platform.uname().node,
        'RASPI-CAPTURE',
    )
    print(conn.connect('150.89.234.242'))

    time0 = cv2.getTickCount()
    list = conn.listPath("pi","Downloads\FaceAPI_old\Tracking")
    count = 0
    for item in list:
        fileName = item.filename
        if fileName == '.' or os.path.splitext(fileName)[1]!='.jpg':
            continue
        count=count+1
        print("process {}".format(item.filename))
        with open('./images/{}'.format(item.filename), 'wb') as file:
            conn.retrieveFile('pi', 'Downloads\FaceAPI_old\Tracking\{}'.format(item.filename), file)
    print((cv2.getTickCount()-time0)/cv2.getTickFrequency())
    print("{}枚処理しました".format(count))
#with io.BytesIO() as file:
    #    conn.retrieveFile('pi', 'Downloads\FaceAPI_old\Tracking\hoge.jpg', file)
    #    file.seek(0)
    #    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    #   img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    #    cv2.imshow("hoge.jpg",img)
    #    cv2.waitKey(0)
