from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from route_menu_screen import RoutesIndexWindow
from route_map_screen import RouteMap

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self,*args):
        return WindowManager()

if __name__ == "__main__":
    MainApp().run()
