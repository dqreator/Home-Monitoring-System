from kivy.clock import Clock
from kivy.event import EventDispatcher


class InitialLoader(EventDispatcher):
    """Implementation of an object meant to perform some loading at app's
    startup. It is responsible for calling functions for theme, language
    and screens loading along with the late initializers in some of the
    manager objects.
    """
    def __init__(self, WindowManager, **kwargs):
        super(InitialLoader, self).__init__(**kwargs)
        self.manager = WindowManager

    def load_screens(self, *args):
        """Most importantly - it loads the primary screens after the
        splash screen schedules it. It also loads the theme and language
        so they can be used on mentioned screens.

        """
        self.manager.load_theme()
        self.manager.load_lang()

        from HomeScreen import HomeScreen
        self.manager.add_widget(HomeScreen(self.manager))

        # Initialize stuff that needs to wait for the UI and other
        # parts of program to load fully first
        # self.manager.fm.late_init()
        # self.manager.dm.update_data()

        # Switch from splash screen to main menu
        Clock.schedule_once(self.manager.get_screen(self.manager.current).skip)
