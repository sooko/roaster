import threading
from kivy.properties import StringProperty ,ListProperty,NumericProperty,ObjectProperty
from kivy.event import EventDispatcher
from serial import Serial
from binascii import hexlify,unhexlify
import time
from kivy.uix.widget import Widget
class Uart(Widget):
    readbaris=StringProperty("")
    ser=Serial()
    l=ListProperty([])
    read_thread =ObjectProperty(None)
    hop=NumericProperty(0)
    def __init__(self,*args,**kwargs):
        super(Uart,self).__init__(*args,**kwargs)
        self.ser.baudrate=19200
        self.ser.port="/dev/ttyUSB0"
        self.ser.timeout=1
        try:
            self.ser.open()
        except:
            pass
        # if not self.read_msg_thread:
        self.read_thread = threading.Thread(target = self.read_msg_thread)
        self.read_thread.start()
    def read_msg_thread(self):
        while True:
            if self.hop==1:
                break
            try:
                if self.ser.is_open==True:
                    r=self.ser.readline().decode()
                    if "stream" in r:
                        s=r.replace("\r\n","")
                        self.readbaris=s      
                else:
                    self.ser.open()
            except:
                self.ser.close()
    def on_readbaris(self,a,b):
        self.ok()
    def ok(self):
        # print(self.readbaris)
        pass
    def write(self,data):
        # print(data)
        if self.ser.is_open:
            self.ser.write(data.encode())
    