from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock

from UtilitiesScreen import (
    on_language, 
    invert_colors,
    change_language,
    )

from HomeScreenUtilities import (
    hide_menu2,
    hide_menu3,
    hide_rv,
    menu2_to_menu3,
    menu3_to_menu2,
    menu3_to_rv,
    rv_to_menu3,
    show_menu3,
    menu3_to_lang_screen,
    lang_screen_to_menu3,
    show_menu2
)

from Buttons import (
    bind_callback,
    unbind_all_callbacks, 
    calculate_nav_buttons, 
    calculate_menu3_buttons_fonts
)

from Images import (
    ICON_MENU_SHUTDOWN,
    ICON_MENU_UTILITIES,
    ICON_MENU_LANGUAGE,
    ICON_MENU_INVERT_TO_DARK,
    ICON_MENU_INVERT_TO_LIGHT,
)
from Strings import (
    MAIN_MENU,
    UTILITIES_MENU, 
)

from Constants import OPACITY_FULL, OPACITY_ZERO

Builder.load_file("screens/menu/home/HomeScreen.kv")


class HomeScreen(Screen):
    """This is an implementation of the class that contains all of the screens
    regarded as "main screens". That means that these screens are all of
    the ones that are available while browsing through the menu up until to
    the moment when user can choose a process he wants to run. If a process
    is chosen the UI switches to "Preprocess Screens".
    """
    utilities_button = ObjectProperty(None)
    top_panel_layout = ObjectProperty(None)

    menu3_layout = ObjectProperty(None)
    menu2_layout = ObjectProperty(None)
    menu1_layout = ObjectProperty(None)

    back_button_background = ObjectProperty(None)
    back_button_label = ObjectProperty(None)
    back_button = ObjectProperty(None)

    next_button_background = ObjectProperty(None)
    next_button_label = ObjectProperty(None)
    next_button = ObjectProperty(None)

    menu3_icon_left = ObjectProperty(None)
    menu3_label_left = ObjectProperty(None)
    menu3_button_left = ObjectProperty(None)

    menu3_icon_middle = ObjectProperty(None)
    menu3_label_middle = ObjectProperty(None)
    menu3_button_middle = ObjectProperty(None)

    menu3_icon_right = ObjectProperty(None)
    menu3_label_right = ObjectProperty(None)
    menu3_button_right = ObjectProperty(None)

    menu2_icon_left = ObjectProperty(None)
    menu2_label_left = ObjectProperty(None)
    menu2_button_left = ObjectProperty(None)

    menu2_icon_right = ObjectProperty(None)
    menu2_label_right = ObjectProperty(None)
    menu2_button_right = ObjectProperty(None)
   
    
    loading_layout = ObjectProperty(None)
    loading_label = ObjectProperty(None)
    
    qr_layout = ObjectProperty(None)
    light_mode_text = ObjectProperty(None)
    camera_settings_text = ObjectProperty(None)
    invert_color_button= ObjectProperty(None)
    invert_color_icon = ObjectProperty(None)
    bottom_panel_layout = ObjectProperty(None)
    bottom_temperature_label = ObjectProperty(None)
    bottom_capacity_label = ObjectProperty(None)
    
    current_screen = StringProperty()


    bottom_material_icon = ObjectProperty(None)
    bottom_crucible_icon = ObjectProperty(None)
    bottom_temperature_icon = ObjectProperty(None)


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

        # self.menu2_icon_left.source = ICON_MENU_SHUTDOWN
        # self.menu2_icon_right.source = ICON_MENU_PROCESS

        # # Prevents calling that function at startup which would hang up the app
        if self.previous_screen is not None:
            calculate_menu3_buttons_fonts(self.menu3_label_left, self.menu3_label_middle, self.menu3_label_right)

        self.menu2_label_left.text = MAIN_MENU["pick"][self.manager.lang]
        self.menu2_label_right.text = MAIN_MENU["place"][self.manager.lang]
        # calculate_menu3_buttons_fonts(self.menu3_label_left, self.menu3_label_middle, self.menu3_label_right)

        calculate_nav_buttons(
            self.back_button_label,
            self.back_button_background,
            self.next_button_label,
            self.next_button_background
        )

        self.back_button.disabled = False
        self.next_button.disabled = False

        unbind_all_callbacks(self.menu2_button_left)
        unbind_all_callbacks(self.menu2_button_right)
        unbind_all_callbacks(self.back_button)

        # unbind_all_callbacks(self.back_button)
        bind_callback(self.menu2_button_left, self.invert_colors)
        bind_callback(self.menu2_button_right, self.laoding_screen)
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
        # self.menu3_icon_left.source = ICON_MENU_LANGUAGE
        # if self.manager.theme == "light":
        #     self.menu3_icon_middle.source = ICON_MENU_INVERT_TO_DARK
        # else:
        #     self.menu3_icon_middle.source = ICON_MENU_INVERT_TO_LIGHT

        # self.menu3_icon_right.source = ICON_MENU_CONSUMABLES

        self.menu3_label_left.text = UTILITIES_MENU["language"][self.manager.lang]
        self.menu3_label_middle.text = UTILITIES_MENU["invert_colors"][self.manager.lang]
        self.menu3_label_right.text = UTILITIES_MENU["consumables"][self.manager.lang]
        calculate_menu3_buttons_fonts(self.menu3_label_left, self.menu3_label_middle, self.menu3_label_right)

        if self.previous_screen == "main":
            self.back_button.disabled = False

        unbind_all_callbacks(self.menu3_button_left)
        unbind_all_callbacks(self.menu3_button_middle)
        unbind_all_callbacks(self.menu3_button_right)
        unbind_all_callbacks(self.back_button)
        # bind_callback(self.menu3_button_left, self.language_screen)
        # bind_callback(self.menu3_button_middle, self.invert_colors)
        # bind_callback(self.menu3_button_right, self.consumables_screen)
        bind_callback(self.back_button, self.main_screen)
        self.set_previous_screen()





    # # --------------------------------- CALLBACKS -------------------------------- #

    def on_pre_enter(self):
        """Pre-enter callback. Depending on the previous_screen variable
        it displays the MainScreen layout or calls a function to clean up
        after a process and display the post-process screen.
        """
        if not hasattr(self, "previous_screen"):
            self.current_screen = ""  # None
            self.previous_screen = None
            hide_menu3(self)
            self.main_screen()
        else:
            # self.finishing_process_screen()
            self.current_screen = ""  # None
            self.previous_screen = None
            hide_menu3(self)
            self.main_screen()


    # # Note: Definitions of functions defined below are in separate files

    # --------------------------------- UTILITIES -------------------------------- #
    # ---------------------------- UtilitiesScreen.py ---------------------------- #

    def on_language(self, *args):
        on_language(self, *args)

    def invert_colors(self, *args):
        invert_colors(self, *args)

    def change_language(self, *args):
        change_language(self, *args)

    # --------------------------------- UTILITIES -------------------------------- #
    # -------------------------- HomeScreenUtilities.py -------------------------- #

    def hide_menu2(self):
        hide_menu2(self)

    def hide_menu3(self):
        hide_menu3(self)

    def hide_rv(self):
        hide_rv(self)

    def menu2_to_menu3(self):
        menu2_to_menu3(self)

    def menu3_to_menu2(self, *args):
        menu3_to_menu2(self)

    def menu3_to_rv(self, *args):
        menu3_to_rv(self)

    def rv_to_menu3(self):
        rv_to_menu3(self)

    def show_menu3(self):
        show_menu3(self)

    def show_menu2(self):
        show_menu2(self)

    def menu3_to_lang_screen(self):
        menu3_to_lang_screen(self)

    def lang_screen_to_menu3(self):
        lang_screen_to_menu3(self)