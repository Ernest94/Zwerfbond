from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.image import Image
from functools import partial
from kivy.network.urlrequest import UrlRequest
from kivy.uix.behaviors import ButtonBehavior

import os

from utils import get_all_data_from_table_for_columnNameIsValue
import GLOBALS

class ImageButton(ButtonBehavior, Image):
    pass

class RoutesIndexScreen(Screen):
    dagindexwindow = StringProperty()

    def __init__(self,**kwargs):
        super(RoutesIndexScreen, self).__init__(**kwargs)

    def on_pre_enter(self):
        Clock.schedule_once(self.set_fields,0)

    def on_leave(self):
        self.ids.header_boxlayout.remove_widget(self.new_image_button)
        self.ids.menu_boxlayout.clear_widgets()

    def set_fields(self,*args):
        self.new_image_button = ImageButton(source='Icon.png', size_hint_y=1, size_hint=(.2,1), allow_stretch=True)
        if not GLOBALS.LOCAL_MAP_DATA_UP_TO_DATE and GLOBALS.BACKEND_AVAILABLE:
                self.new_image_button.bind(on_release=partial(self.switch_screen))
        self.ids.header_boxlayout.add_widget(self.new_image_button)

        self.ids.label_tour_name.text = GLOBALS.LOCAL_MAP_DATA_NAME

        result = get_all_data_from_table_for_columnNameIsValue(GLOBALS.MAP_DATA,"metadata","name","days")
        list_of_days = result[0][1].split(', ')
        for day in list_of_days:
            # new_button = Button(text=day.capitalize(), font_size=36) ##,size_hint=(1,1),md_bg_color=(0, 0, 0, 0.4),text_color= "black",line_color= "red")
            new_button = MDRectangleFlatButton(text=day.capitalize(), font_size=36,size_hint=(1,1),md_bg_color=(0, 0, 0, 0.5),text_color= "white",line_color= "red")
            new_button.bind(on_release=partial(self.on_release_button,day))
            self.ids.menu_boxlayout.add_widget(new_button)

    def on_release_button(self, day,*args, **kwargs):
        self.manager.current = 'routemapscreen'
        self.manager.transition.direction = "left"
        self.dagindexwindow = day

    def switch_screen(self,*args, **kwargs):
        self.manager.current = 'loginscreen'
        self.manager.transition.direction = "right"
