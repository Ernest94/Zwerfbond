from kivy.garden.mapview import MapMarker
from kivy.animation import Animation

class GpsBlinker(MapMarker):
    def blink(self,start):
        # Animation that changes the blink size and opacity
        self.anim = Animation(outer_opacity=0, blink_size=100)
        # When the animation completes, reset the animation, then repeat
        self.anim.bind(on_complete=self.reset)         
        if start:
            self.anim.start(self)
        else:
            self.anim.cancel_all(self)

    def reset(self, *args):
        self.outer_opacity = 1
        self.blink_size = self.default_blink_size
        self.blink(True)