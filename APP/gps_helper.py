from kivy.app import App
from kivy.utils import platform

from utils import get_all_data_from_table_for_columnNameIsValue
import GLOBALS

class GpsHelper():

    def run(self):
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

        #configure gps
        if platform == 'android' or platform == 'ios':
            from plyer import gps
            gps.configure(on_location=self.update_location)#, on_status=self.on_auth_status)
            gps.start(minTime=1000,minDistance=0)

    def update_location(self,*args,**kwargs):
        lat = kwargs['lat']
        lon = kwargs['lon']

        result = get_all_data_from_table_for_columnNameIsValue(GLOBALS.MAP_DATA,'metadata',"name","bounds")
        bbox = result[0][1].split(',')
        if lat>float(bbox[1]) and lat<float(bbox[3]) and lon>float(bbox[0]) and lon<float(bbox[2]):
            gps_tracker = App.get_running_app().root.get_screen("routemap").ids.gps_tracker
            gps_tracker.lat = lat
            gps_tracker.lon = lon
        else:
            print("gps not on map")
            from plyer import gps
            gps.stop()
