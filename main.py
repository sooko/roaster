from kivy.properties import DictProperty,ListProperty,NumericProperty,StringProperty,ObjectProperty,OptionProperty,AliasProperty
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color,Rectangle,Line
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width',1024)
Config.set('graphics', 'height',  600)
Builder.load_file("ml.kv")
Builder.load_file("material.kv")
from chart import *
from kivy.uix.behaviors import ToggleButtonBehavior,ButtonBehavior
from kivy.uix.image import Image,AsyncImage
import json
from ser import Uart
import threading
import time
class TgImg(ToggleButtonBehavior,AsyncImage):
    status=NumericProperty(0)
    type=StringProperty("tg")
    can=ObjectProperty(None)
    rec_size=ListProperty([0,0])
    rec_pos=ListProperty([0,0])
    bg_rgba=ListProperty([1,1,1,1])
    def __init__(self,*args,**kwargs):
        super(TgImg,self).__init__(*args,**kwargs)
        self.source="img/airflow0.png"
        self.color=[0,0,0,1]
    def on_state(self,a,b):
        if self.state=="down":
            # self.color=[1,1,1,1]
            self.status=1
            self.bg_rgba=[.7,.7,.7,1]
        else:
            self.status=0
            self.bg_rgba=[1,1,1,1]
            # self.color=[0,0,0,1]
    def on_status(self,a,b):
        if self.status==1:
            self.state="down"
        else:
            self.state="normal"
    def on_release(self):
        if self.type=="push":
            self.status=0
class BtnStep(ButtonBehavior,AsyncImage):
    status=NumericProperty(0)
    max_status=3
    type=StringProperty("tg")
    def __init__(self,*args,**kwargs):
        super(BtnStep,self).__init__(*args,**kwargs)
        self.source="img/airflow0.png"
        self.color=[0,0,0,1]
    def on_press(self):
        if self.status<self.max_status:
            self.status+=1
        else:
            self.status=0
class Ml(FloatLayout):
    color1=ListProperty([])
    detik=NumericProperty(0)
    menit=NumericProperty(0)
    second=NumericProperty(0)
    waktu=StringProperty("00:00:00")
    state=NumericProperty(0)
    et=NumericProperty(0)
    bt=NumericProperty(0)
    ror=NumericProperty(0)
    protokol=ListProperty([0,0,0,0,0,0,0,0,0,0,0,0])
    toast_eror=StringProperty("")
    state_btn_save=DictProperty({})
    hop=NumericProperty(0)
    # read_thread=ObjectProperty(None)
    uart=Uart()
    data_out=StringProperty("")
    loger={}
    loged={}
    line_et=[]
    line_bt=[]
    line_f=[]
    # line_fb=[]
    # line_etb=[]
    # line_btb=[]
    count=NumericProperty(0)
    storage_num=StringProperty("")
    storage_num_save=StringProperty("")
    plot_area=ObjectProperty(None)
    l_ror=ListProperty([])
    def __init__(self,*args,**kwargs):
        super(Ml,self).__init__(*args,**kwargs)
        Clock.schedule_interval(self.delay,1)
        self.end=self.waktu
        self.uart.ok=self.on_data
        self.list_p=[]
    def delay(self,dt):
        self.ids.chart.major_y=15
        self.ids.chart.major_x=20
        self.plot_area=self.ids.chart.plot_area
        
        try:
            f=open("satate_btn_save.json","r")
            l=json.load(f)
            for i in self.ids.grid_save.children:
                i.warna=l[i.text] 
        except:
            pass
    def start(self,status):
        if status==1:
            self.loger.clear()
            self.count=0
            self.ids.chart.line5.clear()
            self.ids.chart.line6.clear()
            self.line_bt.clear()
            self.line_et.clear()
            self.line_f=[]
            self.detik=0
            self.menit=0
            self.second=0
            self.waktu="{:02d}:{:02d}:{:02d}".format(self.menit,self.detik,self.second)
            
            self.protokol[9]=self.et*10
            self.protokol[10]=self.bt*10
            self.protokol[0]=1
            self.protokol[2]=1
            if self.protokol[1]==1:
                if "00:00:00" in self.loged:
                    l=self.loged["00:00:00"]
                    li=l[1:-2].split(",")
                    print("li")
                    lifloat=[float(i) for i in li]
                    liint=[int(i) for i in lifloat]
                    liint[1]=1
                    self.protokol=liint
                # print(self.loged)
                if self.loged=={}:
                    self.do_toast("no data loaded")
        

        else:
            self.protokol[0]=0
            # self.protokol[2]=0
            self.ids.first.disabled=False
            self.send()

    def on_reset(self):
        self.protokol=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.loger.clear()
        self.count=0
        self.waktu="{:02d}:{:02d}:{:02d}".format(self.menit,self.detik,self.second)
        # self.protokol[9]=self.et*10
        # self.protokol[10]=self.bt*10
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
        self.ids.first.disabled=False
        
    def do_save(self):
        if self.protokol[0]==0 and self.waktu!="00:00:00":
            self.ids.root_save.ilang=.5
        else:
            self.do_toast("belum ada yg perlu disimpan")
    def do_load(self):
        self.ids.root_load.ilang=.5
    def do_toast(self,dt):
        self.ids.toastlabel.warna=[.1,.1,.1,.7]
        self.toast_eror=dt
        Clock.unschedule(self.delaytoast)
        Clock.schedule_once(self.delaytoast,2)
    def delaytoast(self,dt):
        self.toast_eror=""
        self.ids.toastlabel.warna=[0,0,0,0]
    def save(self,a):
        self.storage_num_save=a
        for i in self.ids.grid_save.children:
            self.state_btn_save[i.text]=i.warna
        f=open("satate_btn_save.json","w")
        json.dump(self.state_btn_save,f)
        f.close()
        f=open("{}.json".format(a),"w")
        json.dump({"loger":self.loger,
                    "line_et":self.line_et,
                    "line_bt":self.line_bt,
                    "end":self.waktu,
                    "line_et":self.line_et,
                    "line_bt":self.line_bt,
                    "line_f":self.line_f
                    },f)
        f.close()
        self.ids.root_save.ilang=10
    def load(self,a,b):
        
        if b ==[1,1,1,1]:
            self.storage_num=a
            f=open("{}.json".format(a),"r")
            l=json.load(f)
            self.end=l["end"]
            self.loged=l["loger"]
            self.ids.chart.line1=l["line_et"]
            self.ids.chart.line2=l["line_bt"]
            self.ids.chart.line3=l["line_f"]
        self.ids.root_load.ilang=10
    
    def on_data(self):
        l=self.uart.readbaris.split(",")
        self.et=int(l[2])/10
        self.et=int(l[3])/10
        if self.protokol[0]==1 and self.protokol[1]==0 and int(l[4])==0:
            self.start_time("manual")
        if self.protokol[0]==1 and self.protokol[1]==1 and int(l[4])==1:
            self.start_time("auto")
    def start_time(self,mode):
        if self.menit<20:
            self.second+=1
            if self.second==2:
                self.detik+=1
                if self.detik==60:
                    self.menit+=1
                    self.detik=0
                self.second=0
        self.waktu="{:02d}:{:02d}:{:02d}".format(self.menit,self.detik,self.second)
        if mode=="auto":
            try:
                if self.waktu in self.loged:
                    l=self.loged[self.waktu]
                    li=l[1:-2].split(",")
                    lifloat=[float(i) for i in li]
                    liint=[int(i) for i in lifloat]
                    
                    liint[1]=1
                    self.protokol=liint
                if self.waktu==self.end:
                    # self.protokol[0]=0
                    print("finish")
                    self.protokol=[0,1,0,0,0,0,0,0,0,0,0,0]
            except:
                pass
        if mode=="manual":
            pass
    def lts(self,data):
        return str(data)[1:-1].replace(" ","")
    def on_protokol(self,a,b):
        
        if self.protokol[1]==0 and self.protokol[0]==1: #start manual mode
            self.loger[self.waktu]=self.data_out
        if self.line_f==[] and self.protokol[9]==1:
            self.make_line_f()
            self.ids.first.disabled=True
        if self.protokol[1]==1:
            data=self.lts(self.protokol)
            self.data_out="*{}#\n".format(data)
            self.uart.write(self.data_out)

    def make_line_f(self):
        pa=self.ids.chart.plot_area
        self.line_f=[pa.x+pa.width*self.count/20/60,pa.y,pa.x+pa.width*self.count/20/60,pa.y+pa.height]
        self.ids.chart.line4=self.line_f#[pa.x+pa.width*self.count/20/60,pa.y,pa.x+pa.width*self.count/20/60,pa.y+pa.height]
    def send(self):
        if self.protokol[1]==0:
            data=self.lts(self.protokol)
            self.data_out="*{}#\n".format(data)
            self.uart.write(self.data_out)

    def on_detik(self,a,b):
        self.count+=1
        chart=self.ids.chart
        pa=self.ids.chart.plot_area
        point_et=[pa.x+pa.width*self.count/20/60,pa.y+pa.height*int(self.et)/300]
        point_bt=[pa.x+pa.width*self.count/20/60,pa.y+pa.height*int(self.bt)/300]
        self.line_bt+=point_bt
        self.line_et+=point_et
        chart.line5=self.line_bt
        chart.line6=self.line_et
                
    def stopapp(self):
        self.uart.hop=1
    def on_menit(self,a,b):
        self.l_ror.append(self.bt)
        if len(self.l_ror)==2:
            self.ror=self.l_ror[1]-self.l_ror[0]
            self.l_ror.remove(self.l_ror[0])
class Roaster(App):
    ml=Ml()
    def build(self):
        return self.ml
    def on_stop(self):
        self.ml.stopapp()
if __name__=="__main__":
    Roaster().run()












