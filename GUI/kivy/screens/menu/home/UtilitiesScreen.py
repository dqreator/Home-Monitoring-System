"""Holds definitions of functions used on the "Utilities Screen"
"""
from Buttons import bind_callback, unbind_all_callbacks

from Constants import  LANGUAGES


def invert_colors(self, *args):
    """Inverts the app's color theme.
    """
    if self.manager.theme == "light":
        self.manager.theme = "dark"
    else:
        self.manager.theme = "light"






