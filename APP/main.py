from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.network.urlrequest import UrlRequest
from kivy.core.window import Window
import os

from login_screen import LoginScreen
from route_index_screen import RoutesIndexScreen
from route_map_screen import RouteMapScreen
import GLOBALS
from utils import get_all_data_from_table_for_columnNameIsValue

class WindowManagerWithLoginScreen(ScreenManager):
    pass

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):
    def backend_available(self,req,result):
        GLOBALS.BACKEND_AVAILABLE=True
        GLOBALS.BACKEND_MAP_DATA_NAME = result

    def backend_not_available(self,req,result):
        GLOBALS.BACKEND_AVAILABLE=False

    def build(self,*args):
        Window.size=(375,667)
        request = UrlRequest(GLOBALS.IP_SERVER+"/get_mbtiles_name",on_failure=self.backend_not_available, on_error=self.backend_not_available, on_success=self.backend_available, timeout=2)
        request.wait()
        GLOBALS.LOCAL_MAP_DATA_AVAILABLE = os.path.exists(GLOBALS.MAP_DATA)

        if not GLOBALS.LOCAL_MAP_DATA_AVAILABLE and GLOBALS.BACKEND_AVAILABLE:
            print("Mbtiles does not exist and backend is available: show login screen")
            return WindowManagerWithLoginScreen()
        elif not GLOBALS.LOCAL_MAP_DATA_AVAILABLE and not GLOBALS.BACKEND_AVAILABLE:
            print("Mbtiles does not exist and backend is not available: show login screen")
            return WindowManagerWithLoginScreen()
        elif GLOBALS.LOCAL_MAP_DATA_AVAILABLE and GLOBALS.BACKEND_AVAILABLE:
            GLOBALS.LOCAL_MAP_DATA_NAME = get_all_data_from_table_for_columnNameIsValue(GLOBALS.MAP_DATA,"metadata","name","name")[0][1]
            if GLOBALS.LOCAL_MAP_DATA_NAME != GLOBALS.BACKEND_MAP_DATA_NAME:
                print("Mbtiles exists and backend is available, newer version of mbtiles is available: show login screen")
                return WindowManagerWithLoginScreen()
            elif GLOBALS.LOCAL_MAP_DATA_NAME == GLOBALS.BACKEND_MAP_DATA_NAME:
                print("Newest version of mbtiles exists in the app, backend is available: show route menu screen")
                GLOBALS.LOCAL_MAP_DATA_UP_TO_DATE=True
                return WindowManager()
        elif GLOBALS.LOCAL_MAP_DATA_AVAILABLE and not GLOBALS.BACKEND_AVAILABLE:
            print("Mbtiles file exists in the app and backend is not available: show route menu screen.")
            GLOBALS.LOCAL_MAP_DATA_NAME = get_all_data_from_table_for_columnNameIsValue(GLOBALS.MAP_DATA,"metadata","name","name")[0][1]
            return WindowManager()

if __name__ == "__main__":
    MainApp().run()
