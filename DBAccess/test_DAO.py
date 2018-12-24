from unittest import TestCase
from  DBAccess.DAOBJ import DAO
from datetime import datetime
class TestDAO(TestCase):
    def test_write(self):
        with DAO() as dao:
            dao.write(datetime.now(),"hoge","mesage")
