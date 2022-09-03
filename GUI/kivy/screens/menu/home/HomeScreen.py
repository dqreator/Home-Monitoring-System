from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
import requests, json

from UtilitiesScreen import (
    invert_colors,
    )

from Buttons import (
    bind_callback,
    unbind_all_callbacks, 
)


from Constants import (
    OPACITY_FULL, 
    OPACITY_ZERO, 
    TOPIC_LIGHT_1_C,
    TOPIC_LIGHT_2_C,
    )


Builder.load_file("screens/menu/home/HomeScreen.kv")


class HomeScreen(Screen):

    utilities_button = ObjectProperty(None)
    top_panel_layout = ObjectProperty(None)

    menu3_layout = ObjectProperty(None)
    menu2_layout = ObjectProperty(None)
    menu1_layout = ObjectProperty(None)


    loading_layout = ObjectProperty(None)
    loading_label = ObjectProperty(None)
    current_screen = StringProperty()

    top_panel_button = ObjectProperty(None)
    light_1_icon = ObjectProperty(None)
    light_1_button = ObjectProperty(None)

    temp1_label = ObjectProperty(None)
    hum1_label = ObjectProperty(None)
    light_2_icon = ObjectProperty(None)
    light_2_button = ObjectProperty(None)

    temp2_label = ObjectProperty(None)

    hum2_label = ObjectProperty(None)

    door_icon = ObjectProperty(None)
    motion_1_icon = ObjectProperty(None)
    motion_2_icon = ObjectProperty(None)
    

    def __init__(self, manager, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)


    def set_previous_screen(self, *args):
        """Updates the previous_screen variable.s
        """
        self.previous_screen = self.current_screen

    # ----------------------------- MAIN MENU SCREEN ----------------------------- #

    def main_screen(self, *args):
        """Definition of the "Main Screen".
        """
        self.current_screen = "main"

        unbind_all_callbacks(self.top_panel_button)
        unbind_all_callbacks(self.light_1_button)
        unbind_all_callbacks(self.light_2_button)

        bind_callback(self.top_panel_button, self.invert_colors)
        bind_callback(self.light_1_button, self.toggle_ligth1)
        bind_callback(self.light_2_button, self.toggle_ligth2)
        self.set_previous_screen()

    def laoding_screen(self, *args):
        self.hide_menu2()
        self.loading_layout.opacity = OPACITY_FULL
        self.top_panel_layout.opacity = OPACITY_ZERO
        Clock.schedule_once(self.utilities_screen, 3)


    def shutdown(self, *args):
        """Definition of what happens after the shutdown button is pressed.
        """
        App.get_running_app().stop()
        # os.system('sudo shutdown -h now')

    def utilities_screen(self, *args):
        """Definition of the "Utilities Screen".MAIN_MENU
        """
        self.loading_layout.opacity = OPACITY_ZERO
        self.top_panel_layout.opacity = OPACITY_FULL
        self.show_menu2()
        self.current_screen = "utilities"

        self.set_previous_screen()

    def toggle_ligth1(self, *args):
        if(self.manager.mqtt.light1_status == True):
            self.manager.mqtt.publish(TOPIC_LIGHT_1_C,'0')
        else:
            self.manager.mqtt.publish(TOPIC_LIGHT_1_C,'0')

    def toggle_ligth2(self, *args):
        if(self.manager.mqtt.light2_status == True):
            self.manager.mqtt.publish(TOPIC_LIGHT_2_C,'0')
        else:
            self.manager.mqtt.publish(TOPIC_LIGHT_2_C,'0')






    # # --------------------------------- CALLBACKS -------------------------------- #

    def on_pre_enter(self):
        """Pre-enter callback. Depending on the previous_screen variable
        it displays the MainScreen layout or calls a function to clean up
        after a process and display the post-process screen.
        """
        if not hasattr(self, "previous_screen"):
            self.current_screen = ""  # None
            self.previous_screen = None
            self.main_screen()
        else:
            self.current_screen = ""  # None
            self.previous_screen = None
            self.main_screen()

 


    # # Note: Definitions of functions defined below are in separate files

    # --------------------------------- UTILITIES -------------------------------- #
    # ---------------------------- UtilitiesScreen.py ---------------------------- #


    def invert_colors(self, *args):
        invert_colors(self, *args)


    # --------------------------------- UTILITIES -------------------------------- #
    # -------------------------- HomeScreenUtilities.py -------------------------- #
