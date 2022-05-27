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


from Constants import (
    _C9C9C9,  # COLOR_OFF_LIGHT
    _616161,  # COLOR_ICON_LIGHT, COLOR_BACKGROUND_DARK
    _E6E6E6,  # COLOR_BACKGROUND_LIGHT, COLOR_ICON_DARK
    _CCCCCC,  # COLOR_BACKGROUND_SPINNER_LIGHT, COLOR_MOVING_ACCENT_DARK
    _C4C4C4,  # COLOR_UNDERBAR_LIGHT
    _7A7A7A,  # COLOR_MOVING_ACCENT_LIGHT, COLOR_BACKGROUND_SPINNER_DARK
    _969696,  # COLOR_OFF_DARK
    _929292,  # COLOR_UNDERBAR_DARK
)

from Images import (
    ICON_MENU_INVERT_TO_LIGHT,
    ICON_MENU_INVERT_TO_DARK,
    LOADER_LOADING_IMAGE,
    LOADER_ERROR_IMAGE,
)

from Strings import OTHER_STRINGS

class WindowManager(ScreenManager):
    theme = OptionProperty("light", options=["light", "dark"])
    lang = OptionProperty("en", options=["en", "pl"])

    # Theme properties (init with light theme):
    COLOR_OFF = ListProperty(_C9C9C9)
    COLOR_ICON = ListProperty(_616161)
    COLOR_BACKGROUND = ListProperty(_E6E6E6)
    COLOR_BACKGROUND_SPINNER = ListProperty(_CCCCCC)
    COLOR_UNDERBAR = ListProperty(_C4C4C4)
    COLOR_MOVING_ACCENT = ListProperty(_7A7A7A)

    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

        # Get rid of screen transitions for more snappy UI.
        self.transition = NoTransition()

        # Object which does the screen loading during app initialization.
        self.initialLoader = InitialLoader(self)

        # Get rid of the ugly AsyncImage loading animation
        # and set our own error_image.
        Loader.loading_image = LOADER_LOADING_IMAGE
        Loader.error_image = LOADER_ERROR_IMAGE

    def load_theme(self):
        """Loads theme data from the settings file at startup.
        """
        print("Loading theme")
        # loaded["theme"] = self.theme
        # try:
        #     with open(SETTINGS_FILE, "r+") as file:
        #         loaded = json.load(file)

        #     self.theme = loaded["theme"]

        # except IOError:
        #     # TODO: Settings file read error - add fault report
        #     Logger.exception(OTHER_STRINGS["exception_file_read"][self.lang])

        # # If "theme" key hasn't been found in settings file - add
        # except KeyError:
        #     loaded["theme"] = self.theme

        #     try:
        #         with open(SETTINGS_FILE, "w+") as file:
        #             json.dump(loaded, file)

        #     except IOError:
        #         # TODO: Settings file write error - add fault report
        #         Logger.exception(OTHER_STRINGS["exception_file_write"][self.lang])

    def on_theme(self, *args):
        """Changes the theme at on_theme change and saves selected theme
        type to file so the app starts up with the last theme selected.
        """
        def switch(*args):
            """Wraps UI color change into callable for scheduling.
            """
            if self.theme == "dark":
                self.COLOR_OFF = _969696
                self.COLOR_ICON = _E6E6E6
                self.COLOR_UNDERBAR = _929292
                self.COLOR_MOVING_ACCENT = _CCCCCC
                self.COLOR_BACKGROUND_SPINNER = _7A7A7A
                self.COLOR_BACKGROUND = _616161  # Called last to trigger callbacks

                if self.has_screen("main"):
                    main_screen = self.get_screen("main")
                    if main_screen.current_screen == "utilities":
                        main_screen.menu3_icon_middle.source = ICON_MENU_INVERT_TO_LIGHT
                        main_screen.menu3_button_middle.ripple_fade()  # Prevents a light ripple on dark theme

            elif self.theme == "light":
                self.COLOR_OFF = _C9C9C9
                self.COLOR_ICON = _616161
                self.COLOR_UNDERBAR = _C4C4C4
                self.COLOR_MOVING_ACCENT = _7A7A7A
                self.COLOR_BACKGROUND_SPINNER = _CCCCCC
                self.COLOR_BACKGROUND = _E6E6E6  # Called last to trigger callbacks

                if self.has_screen("main"):
                    main_screen = self.get_screen("main")
                    if main_screen.current_screen == "utilities":
                        main_screen.menu3_icon_middle.source = ICON_MENU_INVERT_TO_DARK
                        main_screen.menu3_button_middle.ripple_fade()  # Prevents a dark ripple on light theme

        Clock.schedule_once(switch)



    def load_lang(self):
        """Loads language data at startup.
        """
        print("Loading lang")



    def on_lang(self, *args):
        """Saves selected language as the one the app will use next time
        it is started. Triggered by self.lang change.
        """
        print("On language")

