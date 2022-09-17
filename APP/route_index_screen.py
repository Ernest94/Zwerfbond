from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from functools import partial
from kivy.network.urlrequest import UrlRequest

import os

from utils import get_all_data_from_table_for_columnNameIsValue
import CONSTANTS

class RoutesIndexScreen(Screen):
    dagindexwindow = StringProperty()

    def __init__(self,**kwargs):
        super(RoutesIndexScreen, self).__init__(**kwargs)

    def on_pre_enter(self):
        Clock.schedule_once(self.set_fields,0)

    def on_leave(self):
        self.ids.boxlayout.clear_widgets()

    def set_fields(self,*args):
        self.request = UrlRequest(CONSTANTS.IP_SERVER+"/get_mbtiles_name")
        self.request.wait()
        if get_all_data_from_table_for_columnNameIsValue(CONSTANTS.MAP_DATA,"metadata","name","name")[0][1] == self.request.result:
            self.ids.image_button.disabled=True
        results = get_all_data_from_table_for_columnNameIsValue(CONSTANTS.MAP_DATA,"metadata","name","name")
        self.ids.label_tour_name.text = results[0][1]

        result = get_all_data_from_table_for_columnNameIsValue(CONSTANTS.MAP_DATA,"metadata","name","days")
        list_of_days = result[0][1].split(', ')
        for day in list_of_days:
            new_button = Button(text=day.capitalize(), font_size=36)
            new_button.bind(on_release=partial(self.on_release_button,day))
            self.ids.boxlayout.add_widget(new_button)

    def on_release_button(self, day,*args, **kwargs):
        self.manager.current = 'routemapscreen'
        self.manager.transition.direction = "left"
        self.dagindexwindow = day

    def switch_screen(self,*args, **kwargs):
        self.manager.current = 'loginscreen'
        self.manager.transition.direction = "right"
