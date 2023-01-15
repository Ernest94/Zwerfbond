import sqlite3;
import time
import os
from kivy.app import App
from kivy.utils import platform
from kivy.network.urlrequest import UrlRequest

import GLOBALS

def get_all_data_from_table_for_columnNameIsValue(database,table,column_name,value):
    if platform == 'ios':
        user_data_dir = App.get_running_app().user_data_dir
        database = os.path.join(user_data_dir, database)
    db_mbtiles = sqlite3.connect(database)
    c_mbtiles = db_mbtiles.cursor()
    sql = "SELECT * FROM "+table+" WHERE "+column_name+" = ?"
    sql_day = (value, )
    c_mbtiles.execute(sql, sql_day)
    myresult = c_mbtiles.fetchall()
    db_mbtiles.close()
    return myresult

def backend_available(req,result):
    GLOBALS.BACKEND_AVAILABLE=True
    GLOBALS.BACKEND_MAP_DATA_NAME = result

def backend_not_available(req,result):
    GLOBALS.BACKEND_AVAILABLE=False

def initialize_app_state():
    request = UrlRequestWithWait(GLOBALS.IP_SERVER+"/get_mbtiles_name",on_failure=backend_not_available, on_error=backend_not_available, on_success=backend_available, timeout=2)
    request.wait(delay=0.5)
    if platform == 'ios':
        user_data_dir = App.get_running_app().user_data_dir
        GLOBALS.LOCAL_MAP_DATA_FILE_PATH = os.path.join(user_data_dir, GLOBALS.LOCAL_MAP_DATA_FILE_PATH)
    GLOBALS.LOCAL_MAP_DATA_AVAILABLE = os.path.exists(GLOBALS.LOCAL_MAP_DATA_FILE_PATH)

class UrlRequestWithWait(UrlRequest):
    # subclassed to use timeout in blocking wait()
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)
        self.start_time = time.time()  # new attribute to keep track of request duration

    def wait(self, delay=0.5):
        # modified While to 'and' timeout not expired
        while (self.resp_status is None) and (self.start_time + self._timeout > time.time()):
            self._dispatch_result(delay)
            time.sleep(delay)
