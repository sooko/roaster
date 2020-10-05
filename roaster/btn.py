from kivy.uix.behaviors.touchripple import  TouchRippleButtonBehavior
from kivy.uix.image import Image,AsyncImage
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior,ToggleButtonBehavior
from kivy.lang import  Builder
Builder.load_string("""
<TgImg>:
    warna:1,1,1,1
    canvas.before:
        Color:
            rgba:self.warna
        Rectangle:
            size:self.size
            pos:self.pos
    img1:""
    img2:""
    on_state:
        self.source=self.img1 if self.state=="down" else self.img2
        root.warna=[1,1,1,.6]if self.state=="down" else [1,1,1,1]
<ButtonImg>:
    warna:1,1,1,1
    canvas.before:
        Color:
            rgba:self.warna
        Rectangle:
            size:self.size
            pos:self.pos
    on_state:
        root.warna=[1,1,1,.6]if self.state=="down" else [1,1,1,1]


""")

class Btn(TouchRippleButtonBehavior,Label):
    pass
class BtnImg(TouchRippleButtonBehavior,Image):
    pass
class TgImg(ToggleButtonBehavior,AsyncImage):
    pass

class ButtonImg(ButtonBehavior,Image):
    pass
class ToggleButtonImg(ToggleButtonBehavior,Image):
    pass
class BtnPush(ButtonImg):
    pass
