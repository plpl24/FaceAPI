import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime as dt
import time


class sp_sheets:
    def __init__(self, sheetName: str) -> None:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('FaceCapRecog-ed25a3a6a0c9.json', scope)
        gc = gspread.authorize(credentials)
        self.wks = gc.open(sheetName).sheet1
        self.row = self.read('D1')
        if self.row == '':
            self.row = 0
        else:
            self.row = int(self.row)

        print("{}に設定されました".format(self.row))



    def write(self, place: str, text: str):
        try:
            print("{}に書き込みます".format(place))
            self.wks.update_acell(place, text)
            currentRow = int(place[1])
            if self.row < currentRow:
                self.row = currentRow
                self.wks.update_acell('D1',currentRow)
            print(currentRow)
        except gspread.exceptions.APIError as e:
            print(e)
            for t in range(30):
                time.sleep(1)
                print(30-t)
            self.write(place, text)

    def read(self, place: str) -> str:

        try:
            return self.wks.acell(place).value
        except gspread.exceptions.APIError as e:
            print(e)
            for t in range(30):
                time.sleep(1)
                print(30-t)
            return self.read(place)

    def get_last_row(self, column: str) -> int:
        return self.row

    def write_datetime(self, place, datetime: dt):
        self.write(place, datetime.strftime('%Y/%m/%d %H:%M:%S:%f'))

# example
# sheet = sp_sheets('faceRecog')
# print(sheet.write('B1','hi'))
# print(sheet.get_last_row('B'))
