from kivy.app import App
from roaster.mainlayout import MainLayout
from kivy.config import Config
Config.set('graphics', 'width',1024)
Config.set('graphics', 'height',  600)
class Roaster(App):
    def build(self):
        return MainLayout()
if __name__=="__main__":
    Roaster().run()
