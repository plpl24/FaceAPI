import pyodbc
from datetime import datetime as dt

database = 'faceDB'
username = 'plpl'
password = 'Raiku1119'


class DAO:

    def __enter__(self):
        self.cnxn = pyodbc.connect('DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % ('AZURE', username, password, database))
        return self

    def write(self,data:dt,name:str,    message:str):
        cursor = self.cnxn.cursor()
        cursor.execute("INSERT INTO dbo.LOG(NAME, TIME, MESSAGE) VALUES(?,?,?);",name,data.strftime('%Y-%m-%d %H:%M:%S'),message)
        self.cnxn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnxn.close()
