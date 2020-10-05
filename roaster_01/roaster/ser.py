from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import platform
import threading
import sys
import time
from kivy.clock import Clock
from serial.tools import list_ports
from serial import Serial
class Ser(Serial):
    device_name_list = []
    def __init__(self,*args,**kwargs):
        super(Ser,self).__init__(*args,**kwargs)
        Clock.schedule_once(self.delay,.1)
    def delay(self,dt):
        self.read_thread = threading.Thread(target = self.read_msg_thread)
        self.read_thread.start()
    def scan(self):
        self.port="/dev/ttyUSB0"
        self.baudrate=19200
    def read_msg_thread(self):
        while True:
            try:
                if self.is_open==True:
                    r=self.readline()
                    if len(r)>2:
                        self.get_data(r)
                else:
                    self.open()
                    time.sleep(1)
            except Exception as e:
                print(e)
                self.close()
                time.sleep(1)
                self.scan()                
    def get_data(self,data):
        pass
    def write_data(self,data):
        if self.is_open:
            self.write(data)