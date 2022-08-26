from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from functools import partial

from utils import get_all_data_from_table_for_columnNameIsValue
import CONSTANTS

class RoutesIndexWindow(Screen):
    dagindexwindow = StringProperty()

    def __init__(self,**kwargs):
        super(RoutesIndexWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.set_fields,0)

    def set_fields(self,*args):
        results = get_all_data_from_table_for_columnNameIsValue(CONSTANTS.MAP_DATA,"metadata","name","name")
        self.ids.label_tour_name.text = results[0][1]

        result = get_all_data_from_table_for_columnNameIsValue(CONSTANTS.MAP_DATA,"metadata","name","days")
        list_of_days = result[0][1].split(', ')
        for day in list_of_days:
            new_button = Button(text=day.capitalize(), font_size=36)
            new_button.bind(on_release=partial(self.on_release_button,day))
            self.ids.boxlayout.add_widget(new_button)

    def on_release_button(self, day,*args, **kwargs):
        self.manager.current = 'routemap'
        self.manager.transition.direction = "left"
        self.dagindexwindow = day
