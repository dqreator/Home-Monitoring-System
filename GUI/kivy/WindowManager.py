from kivy.clock import Clock
from kivy.loader import Loader
from kivy.logger import Logger
from kivy.properties import (
    ListProperty,
    OptionProperty
)
from kivy.uix.screenmanager import (
    ScreenManager, 
    NoTransition
) 
from InitialLoader import InitialLoader
from MqttConnectionManager import MqttConnectionManager

from Constants import (
    _616161,  # COLOR_ICON_LIGHT, COLOR_BACKGROUND_DARK
    _E6E6E6,  # COLOR_BACKGROUND_LIGHT, COLOR_ICON_DARK
)

from Images import (
    LOADER_LOADING_IMAGE,
    LOADER_ERROR_IMAGE,
)

class WindowManager(ScreenManager):
    theme = OptionProperty("dark", options=["light", "dark"])
    lang = OptionProperty("en", options=["en", "pl"])

    # Theme properties (init with light theme):
    COLOR_ICON = ListProperty(_616161)
    COLOR_BACKGROUND = ListProperty(_E6E6E6)

    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

        # Get rid of screen transitions for more snappy UI.
        self.transition = NoTransition()
        
        # Object which takes care of the mqtt communication
        self.mqtt = MqttConnectionManager(self)

        # Object which does the screen loading during app initialization.
        self.initialLoader = InitialLoader(self)

        # and set our own error_image.
        Loader.loading_image = LOADER_LOADING_IMAGE
        Loader.error_image = LOADER_ERROR_IMAGE

    def load_theme(self):
        """Loads theme data from the settings file at startup.
        """
        print("Loading theme")


    def on_theme(self, *args):
        """Changes the theme at on_theme change and saves selected theme
        type to file so the app starts up with the last theme selected.
        """
        def switch(*args):
            """Wraps UI color change into callable for scheduling.
            """
            if self.theme == "dark":
                self.COLOR_ICON = _E6E6E6
                self.COLOR_BACKGROUND = _616161  # Called last to trigger callbacks

            elif self.theme == "light":
                self.COLOR_ICON = _616161
                self.COLOR_BACKGROUND = _E6E6E6  # Called last to trigger callbacks


        Clock.schedule_once(switch)



