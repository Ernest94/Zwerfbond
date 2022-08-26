from kivy.app import App
from kivy.utils import platform

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
        
        if lat>49.994698 and lat<50.249160 and lon>5.274382 and lon<5.849791:
            gps_tracker = App.get_running_app().root.get_screen("routemap").ids.gps_tracker
            gps_tracker.lat = lat
            gps_tracker.lon = lon
        else:
            print("gps not on map")
            from plyer import gps
            gps.stop()
            
            
#    def on_auth_status(self,general_status,status_message):
#        if general_status == 'provider-enabled':
#            pass
#        else:
#            self.open_gps_access_popup()
#
#    def open_gps_access_popup(self):
#        popup = Popup(title="GPS Error", content=Label(text="You need to enable GPS access for the app to function properly"))
#        popup.size_hint = [.8, .8]
#        popup.pos_hint = {'center_x':.5,'center_y':.5}
#        popup.open()
#
    
    
       # try:
           # gps_tracker = App.get_running_app().root.get_screen("routemap").ids.gps_tracker
           # gps_tracker.lat = kwargs['lat']
           # gps_tracker.lon = kwargs['lon']
        #except:
           # print("gps not on map")
           # gps.stop()
            
            
#min_lon, min_lat, max_lon, max_lat = 5.274382,49.994698,5.849791,50.249160            
