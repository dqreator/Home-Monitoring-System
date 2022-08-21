from kivy.clock import Clock
from kivy.event import EventDispatcher


class InitialLoader(EventDispatcher):

    def __init__(self, WindowManager, **kwargs):
        super(InitialLoader, self).__init__(**kwargs)
        self.manager = WindowManager

    def load_screens(self, *args):

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
