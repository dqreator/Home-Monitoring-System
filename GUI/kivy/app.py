#coding=utf-8
import sys 
from kivy.app import App
from kivy.lang import Builder

Builder.load_file("./Backgrounds.kv")
Builder.load_file("./Buttons.kv")
Builder.load_file("./DebugPositionGrid.kv")
Builder.load_file("./Icons.kv")
Builder.load_file("./Labels.kv")
Builder.load_file("./Layouts.kv")


sys.path.append("../images")
sys.path.append("../libraries")
sys.path.append("./screens/menu")
sys.path.append("./screens/menu/home")

from Images import ICON_APP
import SplashScreen 
import WindowManager
import TouchRippleButton


class dqreatorHomeApp(App):
    def build(self):
        self.icon = ICON_APP
        return Builder.load_file("WindowManager.kv")

    def on_stop(self):
        return super().on_stop()