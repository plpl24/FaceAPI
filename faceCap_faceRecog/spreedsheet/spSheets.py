import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime as dt


class sp_sheets:
    def __init__(self, sheetName: str) -> None:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('FaceCapRecog-ed25a3a6a0c9.json', scope)
        gc = gspread.authorize(credentials)
        self.wks = gc.open(sheetName).sheet1

    def write(self, place: str, text: str):
        self.wks.update_acell(place, text)

    def read(self, place: str) -> str:
        return self.wks.acell(place).value

    def get_last_row(self, column: str) -> int:
        row = 0
        while self.read('{}{}'.format(column,row+1)) != '':
            row = row + 1

        return row

    def write_datetime(self,place,datetime:dt):
        self.write(place,datetime.strftime('%Y/%m/%d %H:%M:%S:%f'))

# example
# sheet = sp_sheets('faceRecog')
# print(sheet.write('B1','hi'))
# print(sheet.get_last_row('B'))
