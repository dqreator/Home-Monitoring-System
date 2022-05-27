"""Holds definitions of functions used on the "Utilities Screen"
"""
from Buttons import bind_callback, unbind_all_callbacks, calculate_nav_buttons, calculate_menu3_buttons_fonts

from Strings import  LANGUAGES


def invert_colors(self, *args):
    """Inverts the app's color theme.
    """
    if self.manager.theme == "light":
        self.manager.theme = "dark"
    else:
        self.manager.theme = "light"


def change_language(self, *args):
    """Inverts the app's language.
    """
    if self.manager.lang == "pl":
        self.manager.lang = "en"
    else:
        self.manager.lang = "pl"

def language_screen(self, *args):
    """Language choice screen.
    """

    def _go_back(*args):
        """Hides lang screen layout and switches to previous screen.
        """
        self.lang_screen_to_menu3()
        self.utilities_screen()

    self.menu3_to_lang_screen()
    self.current_screen = "language"
    languages = []
    for language in LANGUAGES:
        languages.append(LANGUAGES[language][self.manager.lang])
    self.lang_spinner.values = languages
    self.lang_spinner.text = LANGUAGES[self.manager.lang][self.manager.lang]
    unbind_all_callbacks(self.back_button)
    bind_callback(self.back_button, _go_back)
    self.set_previous_screen()


def on_language(self, spinner):
    """Called on language selection - updates UI.

    Args:
        spinner (ConsumableSelectionSpinner): Language selection spinner object
    """

    self.manager.lang = list(LANGUAGES)[spinner.values.index(spinner.text)]
    languages = []
    for language in LANGUAGES:
        languages.append(LANGUAGES[language][self.manager.lang])
    self.lang_spinner.values = languages
    self.lang_spinner.text = LANGUAGES[self.manager.lang][self.manager.lang]
    print("saludos")
    # calculate_nav_buttons(
    #     self.back_button_label,
    #     self.back_button_background,
    #     self.next_button_label,
    #     self.next_button_background
    # )


