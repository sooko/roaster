from kivy.properties import DictProperty,ListProperty,NumericProperty,StringProperty,ObjectProperty,OptionProperty,AliasProperty
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color,Rectangle,Line
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width',1024)
Config.set('graphics', 'height',  600)
from kivy.uix.behaviors import ToggleButtonBehavior,ButtonBehavior
from kivy.uix.image import Image,AsyncImage
import json
import threading
import time
from kivy.clock import Clock
import pathlib
path=pathlib.Path(__file__).parent.absolute()
import sys
import os
sys.path.append('{}'.format(path))
Builder.load_file("{}/material.kv".format(path))
Builder.load_file("{}/ml.kv".format(path))
from chart import Chart
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
class PopStorage(FloatLayout):
    btn_choose=DictProperty({})
    def __init__(self, **kwargs):
        super(PopStorage,self).__init__(**kwargs)
    def open(self):
        self.pos_hint={"center_x":.5,"center_y":.5}
    def dissmis(self):
        self.pos_hint={"right":0,"center_y":.5}
    def choose(self,txt):
        pass

class ToggleBtnPopChoose(ToggleButton):
    pass
class ToggleBtnPopSave(ToggleButton):
    pass
class PopChoose(FloatLayout):
    offset=NumericProperty(0)
    cols=NumericProperty(5)
    len_widget=NumericProperty(0)
    type=StringProperty("tg")
    value=NumericProperty(0)

    def __init__(self,*args,**kwargs):
        super(PopChoose,self).__init__(*args,**kwargs)
        self.len_widget=10
    def on_len_widget(self,a,b):
        Clock.schedule_once(self.delay,1)
    def delay(self,dt):
        self.ids.parent_button.clear_widgets()
        if self.type=="tg":
            for i in range(self.len_widget):
                self.ids.parent_button.add_widget(ToggleBtnPopChoose(on_press=self.get_value,text=str(i+self.offset)))
    def open(self):
        self.pos_hint={"center_x":.5,"center_y":.5}
    def dissmis(self):
        self.pos_hint={"center_x":.5,"center_y":10}
    def get_value(self,instance):
        self.value=int(instance.text)

class Logo(Image):
    def __init__(self, **kwargs):
        super(Logo,self).__init__(**kwargs)
        self.source="{}/img/logo.png".format(path)
class TgImg(ToggleButtonBehavior,AsyncImage):
    value=NumericProperty(0)
    type=StringProperty("tg")
    can=ObjectProperty(None)
    rec_size=ListProperty([0,0])
    rec_pos=ListProperty([0,0])
    bg_rgba=ListProperty([1,1,1,1])
    sources=ListProperty(["{}/img/lock on.png".format(path),"{}/img/lock off.png".format(path)])
    path=path
    flag=StringProperty("")
    def __init__(self,*args,**kwargs):
        super(TgImg,self).__init__(*args,**kwargs)
        self.color=[0,0,0,1]
        self.source=self.sources[self.value]
    def on_state(self,a,b):
        if self.state=="down":
            self.value=1
            self.bg_rgba=[.7,.7,.7,1]
        else:
            self.value=0
            self.bg_rgba=[1,1,1,1]
    def on_value(self,a,b):
        if self.value==1:
            self.state="down"
        else:
            self.state="normal"
        self.source=self.sources[self.value]
    def on_release(self):
        if self.type=="push":
            self.value=0
        self.source=self.sources[self.value]
class BtnStep(ButtonBehavior,AsyncImage):
    status=NumericProperty(0)
    max=3
    value=NumericProperty(0)
    color=[0,0,0,1]
    def __init__(self,*args,**kwargs):
        super(BtnStep,self).__init__(*args,**kwargs)
        self.source="{}/img/airflow0.png".format(path,self.value)
    def on_press(self):
        self.value+=1
        if self.value>self.max:
            self.value=0
        self.source="{}/img/airflow{}.png".format(path,self.value)
    def on_value(self,a,b):
        if self.value!=self.max+1:
            self.source="{}/img/airflow{}.png".format(path,self.value)
class BtnLock(TgImg):
    pass
class BtnPlay(TgImg):
    sources=ListProperty(["{}/img/play on.png".format(path),"{}/img/play off.png".format(path)])
class BtnReset(TgImg):
    sources=ListProperty(["{}/img/reset.png".format(path),"{}/img/reset.png".format(path)])
    type="push"
class BtnSave(TgImg):
    type="push"
    sources=ListProperty(["{}/img/save.png".format(path),"{}/img/save.png".format(path)])
class BtnLoad(TgImg):
    type="push"
    sources=ListProperty(["{}/img/load.png".format(path),"{}/img/load.png".format(path)])
class BtnFirst(TgImg):
    type:"push"
    sources=ListProperty(["{}/img/first.png".format(path),"{}/img/first.png".format(path)])
class BtnCharge(TgImg):
    sources=ListProperty(["{}/img/charge on.png".format(path),"{}/img/charge off.png".format(path)])
class BtnDrum(TgImg):
    sources=ListProperty(["{}/img/drum on.png".format(path),"{}/img/drum off.png".format(path)])
class BtnCharge(TgImg):
    sources=ListProperty(["{}/img/charge on.png".format(path),"{}/img/charge off.png".format(path)])
class BtnDisCharge(TgImg):
    sources=ListProperty(["{}/img/discharge on.png".format(path),"{}/img/discharge off.png".format(path)])
class BtnCooling(TgImg):
    sources=ListProperty(["{}/img/cooling on.png".format(path),"{}/img/cooling off.png".format(path)])
class BtnAirFlow(BtnStep):
    pass
class TgMode(ToggleButton):
    value=NumericProperty(0)
class BtnHeater(ButtonBehavior,AsyncImage):
    value=NumericProperty(0)
    max=9
    def __init__(self,*args,**kwargs):
        self.register_event_type("on_open_selection")
        super(BtnHeater,self).__init__(*args,**kwargs)
        self.source="{}/img/heater0.png".format(path,self.value)
    def on_open_selection(self):
        pass
    def on_value(self,a,b):
        self.source="{}/img/heater{}.png".format(path,self.value)
        self.warna=[1,1,1,.7]
        Clock.schedule_once(self.back_color,.15)
    def back_color(self,dt):
        self.warna=[1,1,1,1]
class BtnAirFlow_1(BtnHeater):
    def __init__(self,*args,**kwargs):
        self.register_event_type("on_open_selection")
        super(BtnHeater,self).__init__(*args,**kwargs)
        self.source="{}/img/airflow0.png".format(path)
    def on_value(self,a,b):
        self.source="{}/img/airflow{}.png".format(path,self.value)
        self.warna=[1,1,1,.7]
        Clock.schedule_once(self.back_color,.15)
    def back_color(self,dt):
        self.warna=[1,1,1,1]



























import ast

import ser
class MainLayout(FloatLayout):
    path=path
    plot_area=ObjectProperty(None)
    ror=NumericProperty(0)
    et=NumericProperty(0)
    bt=NumericProperty(0)
    menit=NumericProperty(0)
    detik=NumericProperty(0)
    second=NumericProperty(0)
    serial=ser.Ser()
    protokol=ListProperty([0,0,0,0,0,0,0,0,0,0,0,0])
    dict_control=DictProperty({})
    count=NumericProperty(0)
    play=NumericProperty(0)
    mode=NumericProperty(0)
    sim_count=NumericProperty(0)
    sim_et=NumericProperty(0)
    sim_bt=NumericProperty(0)
    sim_ror=NumericProperty(0)
    sim_mod=NumericProperty(0)
    loger=DictProperty({})
    loged=DictProperty({})
    waktu=StringProperty("00:00:00")
    time_stop=StringProperty("00:00:00")
    time_stoped=StringProperty("00:00:00")
    
    line_et=[]
    line_bt=[]
    line_f=[]
    toast=StringProperty("")
    mcu_mode=NumericProperty(0)
    def __init__(self, **kwargs):
        super(MainLayout,self).__init__(**kwargs)
        Clock.schedule_once(self.delay,1)
        self.serial.get_data=self.get_data
        # Clock.schedule_interval(self.simulator,.05)
    # def load_storage_state(self):
    #     # f=open("{}")
    #     # pass

    def simulator(self,dt):
        self.sim_count+=1
        if self.sim_count==10:
            self.sim_count=0
        self.sim_et+=1
        if self.sim_et==300:
            self.sim_et=0
        self.sim_bt+=1
        if self.sim_bt==300:
            self.sim_bt=0
        self.get_data("stream,{},{},{},{}\r\n".format(self.sim_count,self.sim_et,self.sim_bt,self.sim_mod).encode())
    def delay(self,dt):
        self.ids.chart.major_y=15
        self.ids.chart.major_x=20
        self.plot_area=self.ids.chart.plot_area
        self.load_storage_state()
    def load_storage_state(self):
        try:
            list_storage=os.listdir("{}/storage".format(path))
            for i in self.ids.popsave.ids.parent_btn.children:
                if i.text+".json" in list_storage:
                    i.warna=[1,1,1,1]
            for i in self.ids.popload.ids.parent_btn.children:
                if i.text+".json" in list_storage:
                    i.warna=[1,1,1,1]
        except:
            pass


    def get_data(self,data):
        if b'stream' in data:
            
            
            data=data.decode()
            l=data.split(",")
            self.et=float(l[2])/10
            self.bt=float(l[3])/10
            self.ror=float(l[4])/10
            self.mcu_mode=int(l[5])
            if self.protokol[0]==1 and self.mcu_mode==0 and self.protokol[1]==0:
                self.waktu="{:02d}:{:02d}:{:02d}".format(self.menit,self.detik,self.second)
                if self.menit<=20:
                    self.second+=1
                    if self.second==2:
                        self.detik+=1
                        self.second=0
                    if self.detik==60:
                        self.menit+=1
                        self.detik=0                    
                if self.menit==20:
                    self.protokol[0]=0



            if self.protokol[0]==1 and self.mcu_mode==1:
                self.waktu="{:02d}:{:02d}:{:02d}".format(self.menit,self.detik,self.second)
                if self.menit<=20:
                    self.second+=1
                    if self.second==2:
                        self.detik+=1
                        self.second=0
                    if self.detik==60:
                        self.menit+=1
                        self.detik=0                    
                if self.menit==20:
                    self.protokol[0]=0
                if self.waktu in self.loged:
                    out_auto=self.loged[self.waktu]#.replace("*","[").replace("#","]")
                    l_out_auto=list(out_auto)
                    l_out_auto[3]="1"
                    ready_out="".join(l_out_auto)
                    self.serial.write_data(ready_out.encode())
                    p=ready_out.replace("*","[").replace("#","]")
                    self.protokol=ast.literal_eval(p)
                if self.waktu==self.time_stoped:
                    self.protokol[0]=0



        
    def on_detik(self,a,b):
        self.count+=1
        chart=self.ids.chart
        pa=self.ids.chart.plot_area
        point_et=[int(pa.x+pa.width*self.count/20/60),int(pa.y+pa.height*int(self.et)/300)]
        point_bt=[int(pa.x+pa.width*self.count/20/60),int(pa.y+pa.height*int(self.bt)/300)]
        self.line_bt+=point_bt
        self.line_et+=point_et
        chart.line5=self.line_bt
        chart.line6=self.line_et
    def make_line_f(self):
        pa=self.ids.chart.plot_area
        self.line_f=[pa.x+pa.width*self.count/20/60 ,pa.y, pa.x+pa.width*self.count/20/60, pa.y+pa.height]
        self.ids.chart.line4=self.line_f#[pa.x+pa.width*self.count/20/60,pa.y,pa.x+pa.width*self.count/20/60,pa.y+pa.height]
    def lts(self,data):
        return str(data)[1:-1].replace(" ","")
    def prepare_to_send(self):
        if self.protokol[1]==0:
            data_ready="*"+self.lts(self.protokol)+"#"+"\n"
            print(data_ready)
            if self.protokol[0]==1 and self.protokol[1]==0:
                self.loger[self.waktu]=data_ready
            self.serial.write_data(data_ready.encode())   
        
    def play(self):
        if self.protokol[0]==1:
            self.count=0
            self.detik=0
            self.second=0
            self.menit=0
            self.loger.clear()
            self.protokol[2]=1
            self.protokol[10]=self.et
            self.protokol[11]=self.bt
            self.line_bt=[]
            self.line_et=[]
            self.line_f=[]
            self.ids.chart.line4=[]
            self.ids.chart.line5=[]
            self.ids.chart.line6=[]
        

        else:
            self.time_stop=self.waktu
        data_ready="*"+self.lts(self.protokol)+"#"+"\n"
        print(data_ready)
        self.serial.write_data(data_ready.encode())
    def set_mode(self):
        data_ready="*"+self.lts(self.protokol)+"#"+"\n"
        self.serial.write_data(data_ready.encode())
    def auto_send(self):
        pass
    def reset(self):
        self.ids.first_btn.disabled=False
        self.protokol=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.count=0
        self.detik=0
        self.menit=0
        self.second=0
        self.line_bt=[]
        self.line_et=[]
        self.line_f=[]
        self.ids.chart.line1=[]
        self.ids.chart.line2=[]
        self.ids.chart.line3=[]
        self.ids.chart.line4=[]
        self.ids.chart.line5=[]
        self.ids.chart.line6=[]
    def on_protokol(self,a,b):
        self.mode=self.protokol[1]
    def do_save(self):
        if self.detik==0 and self.menit==0:
            self.do_toast("no data to save",time_out=1)
        elif self.protokol[0]==1:
            self.do_toast("please sop first",time_out=1)
        else:
            self.ids.popsave.open()
    def do_toast(self,data,time_out=2):
        self.toast=data 
        Clock.schedule_once(self.clear_toast,time_out)
        print(self.toast)
    def clear_toast(self,dt):
        self.toast=""
    def save(self,instance):
        self.ids.popsave.dissmis()
        d={"loger":self.loger,"line_et":self.line_et,"line_bt":self.line_bt,"stop":self.time_stop,"line_f":self.line_f}
        f=open("{}/storage/{}.json".format(path,instance.text),"w")
        json.dump(d,f,indent=4)
        self.load_storage_state()
    def load(self,instance):
        self.ids.popload.dissmis()
        if instance.warna==[1,1,1,1]:
            f=open("{}/storage/{}.json".format(path,instance.text),"r")
            storage=json.load(f)            
            self.loged=storage["loger"]
            self.time_stoped=storage["stop"]
            self.ids.chart.line1=storage["line_et"]
            self.ids.chart.line2=storage["line_bt"]
            self.ids.chart.line3=storage["line_f"]
            self.ids.btnload.flag=instance.text
