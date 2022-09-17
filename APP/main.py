from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.network.urlrequest import UrlRequest
import os

from login_screen import LoginScreen
from route_index_screen import RoutesIndexScreen
from route_map_screen import RouteMapScreen
import CONSTANTS
from utils import get_all_data_from_table_for_columnNameIsValue

class WindowManagerWithLoginScreen(ScreenManager):
    pass

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self,*args):
        if not os.path.exists(CONSTANTS.MAP_DATA):
            print("Mbtiles does not exist: show login screen")
            return WindowManagerWithLoginScreen()

        request = UrlRequest(CONSTANTS.IP_SERVER+"/get_mbtiles_name")
        request.wait()
        if get_all_data_from_table_for_columnNameIsValue(CONSTANTS.MAP_DATA,"metadata","name","name")[0][1] == request.result:
            print("mbtiles are up-to-date")
            return WindowManager()
        else:
            print("Newer version of mbtiles is available: show login screen")
            return WindowManagerWithLoginScreen()

if __name__ == "__main__":
    MainApp().run()
