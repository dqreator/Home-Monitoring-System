import threading
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from time import sleep
from kivy.properties import ObjectProperty

Builder.load_file("screens/menu/SplashScreen.kv")


class SplashScreen(Screen):
    """Implements a splash screen which is shown at app's startup.
    """
    loading = ObjectProperty(None)

    def on_enter(self):
        """Defines the behavior after entering the screen (at least in theory).
        It turns out that this function might be called when this screen is
        not actually displayed. This is why the screen loading scheduled below
        is meant to start after 5 seconds.
        """
        # Start the screen loading after 5 seconds, to let the
        # program render and display this screen.
        # If a way to check if the screen does actually display the
        # required content here is found, the load_screens() function
        # should be called after that check returns true.
        Clock.schedule_once(self.manager.initialLoader.load_screens, 4)
        self.dots = 0
        self.loading = Clock.schedule_once(self.loading_screen)

    def loading_screen(self, *args):
        """Implements an "animation" of a loading text with
        dots being added to it repeatadly. It is being shown
        until the skip() function is called.
        """
        # Even though the loading animation is exclusively done
        # on the other thread, it's still a bit stuttery (because
        # the main thread is responsible for displaying it). Maybe
        # setting a longer sleep time would mitigate this effect.
        def _loading_screen():
            while self.dots > -1:
                if self.dots == 0:
                    self.loading.text = "    LOADING"
                elif self.dots == 1:
                    self.loading.text = "    LOADING."
                elif self.dots == 2:
                    self.loading.text = "    LOADING.."
                elif self.dots == 3:
                    self.loading.text = "    LOADING..."

                if self.dots < 3:
                    self.dots += 1
                else:
                    self.dots = 0
                sleep(0.5)

        threading.Thread(target=_loading_screen).start()

    def skip(self, *args):
        """Stops the thread showing the "LOADING" texts
        and changes the current screen to the main one.
        """
        self.dots = -1  # Stop the thread
        self.manager.current = "home"
        # Remove this screen since it's no longer needed
        del self.manager.initialLoader
