from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock

import json
import os

from utils import get_all_data_from_table_for_columnNameIsValue
import GLOBALS
from route_index_screen import RoutesIndexScreen

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def on_pre_enter(self):
        Clock.schedule_once(self.set_dynamic_layout,0)
        if not GLOBALS.LOCAL_MAP_DATA_UP_TO_DATE and GLOBALS.LOCAL_MAP_DATA_AVAILABLE:
            Clock.schedule_once(self.set_DontDownloadOption,0)
            print("local map data not up to date")

    def set_dynamic_layout(self, *args,**kwargs):
        self.ids.download_map_label.text = "Voer het wachtwoord in, om de [b]"+GLOBALS.BACKEND_MAP_DATA_NAME+"[/b] kaart te downloaden:"

    def set_DontDownloadOption(self, *args,**kwargs):
        self.ids.cancel_button.opacity = 1
        self.ids.cancel_button.disabled = False

    def switch_screen(self, *args,**kwargs):
        self.ids.password_input.error = False
        self.manager.current = 'routesindexscreen'
        self.manager.transition.direction = "left"

    def new_map_data_downloaded(self, *args,**kwargs):
        GLOBALS.LOCAL_MAP_DATA_AVAILABLE = True
        GLOBALS.LOCAL_MAP_DATA_UP_TO_DATE = True
        GLOBALS.LOCAL_MAP_DATA_NAME = get_all_data_from_table_for_columnNameIsValue(GLOBALS.MAP_DATA,"metadata","name","name")[0][1]
        self.switch_screen()

    def verify_password(self, *args):
        self.ids.download_button.disabled = True
        if GLOBALS.LOCAL_MAP_DATA_AVAILABLE:
            self.ids.cancel_button.disabled = True
        headers = {'Content-type': 'application/json','Accept': 'text/plain'}
        values = {'password':self.ids.password_input.text}
        params = json.dumps(values)
        password_req = UrlRequest(GLOBALS.IP_SERVER+"/verify", req_body=params, req_headers=headers)
        password_req.wait()
        if password_req.result=="1":
            print("password is correct")
            self.ids.password_input.error = False
            request = UrlRequest(GLOBALS.IP_SERVER+"/get_mbtiles",file_path='map_data_downloaded.mbtiles',chunk_size=8192,on_progress=self.update_progress_bar,on_success=self.new_map_data_downloaded,on_error=self.print_error)
            request.wait()
        else:
            print("wrong password")
            self.ids.password_input.error = True
            self.ids.download_button.disabled = False
            if GLOBALS.LOCAL_MAP_DATA_AVAILABLE:
                self.ids.cancel_button.disabled = False

    def print_error(self,request,error):
        print("An error happened: "+str(error))

    def update_progress_bar(self,request,current_size,total_size):
        self.ids.progress_bar.value = current_size/total_size
