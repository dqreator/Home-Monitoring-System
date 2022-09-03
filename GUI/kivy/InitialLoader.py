from kivy.clock import Clock
from kivy.event import EventDispatcher


class InitialLoader(EventDispatcher):

    def __init__(self, WindowManager, **kwargs):
        super(InitialLoader, self).__init__(**kwargs)
        self.manager = WindowManager

    def load_screens(self, *args):

        from HomeScreen import HomeScreen
        self.manager.add_widget(HomeScreen(self.manager))


        Clock.schedule_once(self.manager.get_screen(self.manager.current).skip)
