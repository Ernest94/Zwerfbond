from kivy.app import App
from kivy.utils import platform
from plyer import gps
from kivymd.uix.dialog import MDDialog
from kivy.clock import mainthread
from gps_blinker import GpsBlinker

from utils import get_all_data_from_table_for_columnNameIsValue
import GLOBALS

class GpsHelper():
   
    def __init__(self):
        self.gps_tracker = None

    def run(self):
        self.gps_tracker = App.get_running_app().root.get_screen("route_map_screen").ids.gps_tracker
        self.gps_tracker.blink()

        #ask permission; android only        
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            def callback(permissions, results):
                if all([res for res in results]):
                    print("Got all permissions")
                else:
                    print("Did not get all permissions")
            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)
            
        if platform == 'android' or platform == 'ios':
            try:
                gps.configure(on_location=self.update_location)
                gps.start(minTime=1000,minDistance=0)
            except NotImplementedError:
                import traceback
                traceback.print_exc()
                self.gps_status = 'GPS is not implemented for your platform'

    @mainthread
    def update_location(self,**kwargs):
        lat = kwargs['lat']
        lon = kwargs['lon']
        print(lat,lon)

        result = get_all_data_from_table_for_columnNameIsValue(GLOBALS.LOCAL_MAP_DATA_FILE_PATH,'metadata',"name","bounds")
        bbox = result[0][1].split(',')
        print(bbox)
        if lat>float(bbox[1]) and lat<float(bbox[3]) and lon>float(bbox[0]) and lon<float(bbox[2]):
            self.gps_tracker = App.get_running_app().root.get_screen("route_map_screen").ids.gps_tracker
            print(self.gps_tracker)
            self.gps_tracker.lat = lat
            self.gps_tracker.lon = lon
        else:
            print("gps not on map")
            gps.stop()

    def open_gps_access_popup(self):
        dialog = MDDialog(title="GPS Error", text="You need to enable GPS access for the app to function properly")
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()