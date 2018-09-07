import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
        row = 1
        while self.read('{}{}'.format(column,row)) != '':
            row = row + 1

        return row


sheet = sp_sheets('faceRecog')
print(sheet.get_last_row('B'))
