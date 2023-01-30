from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from login_screen import LoginScreen
from route_index_screen import RoutesIndexScreen
from route_map_screen import RouteMapScreen
from utils import get_all_data_from_table_for_columnNameIsValue, initialize_app_state
import GLOBALS

class MainApp(MDApp):
    def build(self,*args):
        initialize_app_state()
        self.screen_manager = ScreenManager()

        if not GLOBALS.LOCAL_MAP_DATA_AVAILABLE and GLOBALS.BACKEND_AVAILABLE:
            print("Mbtiles does not exist and backend is available: show login screen")
            self.screen_manager.add_widget(LoginScreen(name='login_screen'))
        elif not GLOBALS.LOCAL_MAP_DATA_AVAILABLE and not GLOBALS.BACKEND_AVAILABLE:
            print("Mbtiles does not exist and backend is not available: show login screen")
            self.screen_manager.add_widget(LoginScreen(name='login_screen'))
        elif GLOBALS.LOCAL_MAP_DATA_AVAILABLE and not GLOBALS.BACKEND_AVAILABLE:
            print("Mbtiles file exists in the app and backend is not available: show route menu screen.")
            GLOBALS.LOCAL_MAP_DATA_NAME = get_all_data_from_table_for_columnNameIsValue(GLOBALS.LOCAL_MAP_DATA_FILE_PATH,"metadata","name","name")[0][1]
        elif GLOBALS.LOCAL_MAP_DATA_AVAILABLE and GLOBALS.BACKEND_AVAILABLE:
            GLOBALS.LOCAL_MAP_DATA_NAME = get_all_data_from_table_for_columnNameIsValue(GLOBALS.LOCAL_MAP_DATA_FILE_PATH,"metadata","name","name")[0][1]
            if GLOBALS.LOCAL_MAP_DATA_NAME != GLOBALS.BACKEND_MAP_DATA_NAME:
                print("Mbtiles exists and backend is available, newer version of mbtiles is available: show login screen")
                self.screen_manager.add_widget(LoginScreen(name='login_screen'))
            elif GLOBALS.LOCAL_MAP_DATA_NAME == GLOBALS.BACKEND_MAP_DATA_NAME:
                print("Newest version of mbtiles exists in the app, backend is available: show route menu screen")
                GLOBALS.LOCAL_MAP_DATA_UP_TO_DATE=True

        self.screen_manager.add_widget(RoutesIndexScreen(name='routes_index_screen'))
        self.screen_manager.add_widget(RouteMapScreen(name='route_map_screen'))
        return self.screen_manager

if __name__ == "__main__":
    MainApp().run()

