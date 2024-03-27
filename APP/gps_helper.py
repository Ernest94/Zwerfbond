from kivy.app import App
from kivy.utils import platform
from plyer import gps
from kivy.clock import mainthread

class GpsHelper():
   
    def __init__(self):
        self.gps_tracker = None

    def configure(self):
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
            except NotImplementedError:
                import traceback
                traceback.print_exc()

    @mainthread
    def start(self):
        if platform == 'android' or platform == 'ios':
            try:
                gps.start(minTime=1000,minDistance=0)
            except NotImplementedError:
                import traceback
                traceback.print_exc()        

    @mainthread
    def update_location(self,**kwargs):
        if App.get_running_app().root.current_screen.name=="route_map_screen":
            lat = kwargs['lat']
            lon = kwargs['lon']
            self.gps_tracker = App.get_running_app().root.get_screen("route_map_screen").ids.gps_tracker
            self.gps_tracker.lat = lat
            self.gps_tracker.lon = lon
            App.get_running_app().root.get_screen("route_map_screen").ids.mapview.trigger_update(True)