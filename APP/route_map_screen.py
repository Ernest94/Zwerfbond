from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.garden.mapview import MapView
from mapview.mbtsource import MBTilesMapSource

from route_drawer_helper import LineMapLayer
from gps_helper import GpsHelper
from utils import get_all_data_from_table_for_columnNameIsValue
import GLOBALS

class RouteMapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        GpsHelper().run()

    def on_enter(self):
        Clock.schedule_once(self.build_map,0)

    def build_map(self,*args):
        source = MBTilesMapSource(GLOBALS.LOCAL_MAP_DATA_FILE_PATH)
        self.ids.mapview.map_source = source
        self.layer = LineMapLayer(GLOBALS.DAG)
        self.ids.mapview.add_layer(self.layer, mode="scatter")   # window scatter

        results = get_all_data_from_table_for_columnNameIsValue(GLOBALS.LOCAL_MAP_DATA_FILE_PATH,"route_coordinates","day",GLOBALS.DAG)
        coordinates_list = eval(results[0][1][1:-1])

        self.ids.mapview.center_on(coordinates_list[1],coordinates_list[0])
        self.ids.eind_marker.lat = coordinates_list[-1]
        self.ids.eind_marker.lon = coordinates_list[-2]+0.0003
        self.ids.label_eind_marker.text = f"Eind {GLOBALS.DAG}"

        #add button to return to menu
        self.button_menu = Button(text="Menu", size_hint=(0.15,0.06),pos_hint={'x':0, 'y':0.94},font_size=30)
        self.button_menu.bind(on_release=self.switch_screen)
        self.add_widget(self.button_menu)

        # add button to recentre on GPS or on start of route
        result = get_all_data_from_table_for_columnNameIsValue(GLOBALS.LOCAL_MAP_DATA_FILE_PATH,'metadata',"name","bounds")
        bbox = result[0][1].split(',')
        self.button_gps = Button(size_hint=(0.12,0.08),pos_hint={'x':0.05,'y':0.03},background_normal='recentre_gps_icon.png',background_down='recentre_gps_icon_down.png')
        if self.ids.gps_tracker.lat>float(bbox[1]) and self.ids.gps_tracker.lat<float(bbox[3]) and self.ids.gps_tracker.lon>float(bbox[0]) and self.ids.gps_tracker.lon<float(bbox[2]):
            self.button_gps.bind(on_press=self.center_map_on_gps)
        else:
            self.button_gps.bind(on_press=self.center_map_on_route)
        self.add_widget(self.button_gps)

    def switch_screen(self, *args):
        self.manager.current = 'routes_index_screen'
        self.manager.transition.direction = "right"

    # # add button to get route-info
    # self.button_info = Button(text="Route""\n""  Info", size_hint=(0.15,0.08),pos_hint={'x':1-0.15, 'y':0.92},font_size=30)
    # self.button_info.bind(on_release=self.route_info_popup)
    # self.add_widget(self.button_info)

    # def route_info_popup(self,*args):
    #     results = get_all_data_from_table_for_day(GLOBALS.LOCAL_MAP_DATA_FILE_PATH,"route_info",GLOBALS.DAG)
    #     popup = Popup(
    #             title=results[0][1],
    #             content=Label(text=results[0][2],
    #                     text_size=(self.width*0.5,self.width*0.6),
    #                     halign='left',
    #                     valign='top'),
    #             size_hint=(0.65,0.6),
    #             pos_hint={'x':0.2, 'y':0.2})
    #     popup.open()

    def center_map_on_gps(self,*args):
        self.ids.mapview.center_on(self.ids.gps_tracker.lat,self.ids.gps_tracker.lon)

    def center_map_on_route(self,*args):
        results = get_all_data_from_table_for_columnNameIsValue(GLOBALS.LOCAL_MAP_DATA_FILE_PATH,"route_coordinates","day",GLOBALS.DAG)
        coordinates_list = eval(results[0][1][1:-1])
        self.ids.mapview.center_on(coordinates_list[1],coordinates_list[0])

    def on_leave(self):
        self.ids.mapview.remove_layer(self.layer)
        self.ids.mapview.zoom = 16
