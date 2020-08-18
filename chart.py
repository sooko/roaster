from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

Builder.load_string("""
<Kotak>:
    canvas:
        Color:
            rgba:0,0,0,1
        Line:
            rectangle:(self.x,self.y,self.width,self.height)
<Xlabel>:
    color:0,0,0,1
    font_size:dp(15)
<Ylabel>:
    color:0,0,0,1
    font_size:dp(15)
<Chart>:
    plot_area:plot_area
    pos_hint:{"center_x":.5,"center_y":.5}
    FloatLayout
        pos_hint:{"center_x":.5,"center_y":.5}
        canvas.before:
            Color:
                rgba:1,1,1,1
            Rectangle:
                size:self.size
                pos:self.pos
        BoxLayout
            pos_hint:{"x":0,"y":0}
            size_hint:None,None
            size:self.parent.size[0]-dp(10),self.parent.size[1]-dp(10)
            BoxLayout:
                orientation:"vertical"
                size_hint:None,1
                width:dp(30)
                BoxLayout:
                    orientation:"vertical"
                    id:root_y_label
                    canvas.before:
                        PushMatrix:
                        Translate:
                            y:(self.height/root.major_y/2)
                    canvas.after:
                        PopMatrix:
                Label
                    text:"0"
                    font_size:dp(15)
                    color:0,0,0,1
                    size_hint:1,None
                    height:dp(20)
            BoxLayout:
                orientation:"vertical"
                size_hint:1,1
                FloatLayout
                    Widget:
                        pos_hint:{"center_x":.5,"center_y":.5}
                        id:plot_area
                        canvas:
                            Color:
                                rgba:0,.5,.5,1
                            Line:
                                width:dp(3)
                                points:root.line1
                            Color:
                                rgba:0,1,1,1
                            Line:
                                width:dp(3)
                                points:root.line2
                            Color:
                                rgba:1,1,0,1
                            Line:
                                width:dp(3)
                                points:root.line3

                            Color:
                                rgba:0,1,0,1
                            Line:
                                width:dp(3)
                                points:root.line4
                            Color:
                                rgba:1,0,0,1
                            Line:
                                width:dp(3)
                                points:root.line5
                            Color:
                                rgba:0,0,1,1
                            Line:
                                width:dp(3)
                                points:root.line6
                    BoxLayout
                        pos_hint:{"center_x":.5,"center_y":.5}
                        id:root_kotak   
                    BoxLayout
                        orientation:"vertical"
                        pos_hint:{"center_x":.5,"center_y":.5}
                        id:root_kotak_y   
                BoxLayout:
                    id:root_x_label
                    size_hint:1,None
                    height:dp(25)
                    canvas.before:
                        PushMatrix:
                        Translate:
                            x:(self.width/root.major_x/2)
                    canvas.after:
                        PopMatrix:
                            
 """)

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
class Kotak(Widget):
    pass
class Xlabel(Label):
    pass
class Ylabel(Label):
    pass
from kivy.uix.button import Button
from kivy.properties import StringProperty,NumericProperty,ListProperty
class Chart(FloatLayout):
    major_x=NumericProperty(1)
    major_y=NumericProperty(1)
    line1=ListProperty([])
    line2=ListProperty([])
    line3=ListProperty([])
    line4=ListProperty([])
    line5=ListProperty([])
    line6=ListProperty([])
    def __init__(self,*args,**kwargs):
        super(Chart,self).__init__(*args,**kwargs)
    def on_major_x(self,a,b):
        self.ids.root_kotak.clear_widgets()
        self.ids.root_x_label.clear_widgets()
        for i in range(self.major_x):
            self.ids.root_kotak.add_widget(Kotak())
            if self.major_x<=40:
                self.ids.root_x_label.add_widget(Xlabel(text=str(i+1)))
            else:
                self.ids.root_x_label.add_widget(Xlabel(text="I"))
    def on_major_y(self,a,b):
        self.ids.root_y_label.clear_widgets()
        self.ids.root_kotak_y.clear_widgets()
        for i in range(self.major_y):
            self.ids.root_y_label.add_widget(Ylabel(text=str((self.major_y-i)*20)))
            self.ids.root_kotak_y.add_widget(Kotak())
    
        