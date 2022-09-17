from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock

import json
import os

from utils import get_all_data_from_table_for_columnNameIsValue
import CONSTANTS
from route_index_screen import RoutesIndexScreen

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.request = UrlRequest(CONSTANTS.IP_SERVER+"/get_mbtiles_name")
        self.request.wait()
        if os.path.exists(CONSTANTS.MAP_DATA):
            if get_all_data_from_table_for_columnNameIsValue(CONSTANTS.MAP_DATA,"metadata","name","name")[0][1] != self.request.result:
                Clock.schedule_once(self.set_DontDownloadOption,0)

    def on_pre_enter(self):
        Clock.schedule_once(self.set_dynamic_layout,0)

    def set_dynamic_layout(self, *args,**kwargs):
        self.ids.download_map_label.text = "Voer het wachtwoord in om de kaart van "+self.request.result+" te downloaden:"

    def set_DontDownloadOption(self, *args,**kwargs):
        # self.ids.cancel_button = MDRaisedButton(text="Kaart niet downloaden",font_size=24,font_style='Body1',pos_hint= {"center_x": .5})
        self.ids.cancel_button.opacity = 1
        self.ids.cancel_button.disabled = False

    def switch_screen(self, *args,**kwargs):
        self.manager.current = 'routesindexscreen'
        self.manager.transition.direction = "left"

    def verify_password(self, *args):
        self.ids.download_button.disabled = True
        if os.path.exists(CONSTANTS.MAP_DATA):
            self.ids.cancel_button.disabled = True
        headers = {'Content-type': 'application/json','Accept': 'text/plain'}
        values = {'password':self.ids.password_input.text}
        params = json.dumps(values)
        password_req = UrlRequest(CONSTANTS.IP_SERVER+"/verify", req_body=params, req_headers=headers)
        password_req.wait()
        if password_req.result=="1":
            print("password is correct")
            self.ids.error_message.text = ''
            request = UrlRequest(CONSTANTS.IP_SERVER+"/get_mbtiles",file_path='map_data_downloaded.mbtiles',chunk_size=8192,on_progress=self.update_progress_bar,on_success=self.switch_screen,on_error=self.print_error)
            request.wait()
        else:
            print("wrong password")
            self.ids.error_message.text = "Kan kaart niet downloaden. Mogelijk is het ingevoerde wachtwoord niet correct."
            self.ids.download_button.disabled = False
            if os.path.exists(CONSTANTS.MAP_DATA):
                self.ids.cancel_button.disabled = False

    def print_error(self,request,error):
        print("An error happened: "+str(error))

    def update_progress_bar(self,request,current_size,total_size):
        self.ids.progress_bar.value = current_size/total_size
