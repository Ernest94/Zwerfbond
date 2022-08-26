from kivy.uix.popup import Popup
from kivy.uix.button import Label

def RouteInfoPopUp(self):
    popup = Popup(content=Label(text='24 km''/n''Van Chabrehez naar Houffalize''/n/''Vandaag lopen we in zuidelijke richting. Het eerste deel door de natuur en het tweede deel voornamelijk door dorpjes'), size_hint=(None, None), size=(400, 400))
    popup.open()
