"""UI elements' visibility modifying functions that
are called from the MainScreen class.
"""

from Constants import OPACITY_FULL, OPACITY_ZERO


def menu3_to_menu2(self, *args):
    """Hide 3 icon menu, disable its buttons
    and enable 2 icon menu with its buttons instead.
    """
    self.menu3_button_left.hidden = True
    self.menu3_button_middle.hidden = True
    self.menu3_button_right.hidden = True
    self.menu2_button_left.disabled = False
    self.menu2_button_right.disabled = False


def menu2_to_menu3(self):
    """Hide 2 icon menu, disable its buttons
    and enable 3 icon menu with its buttons instead.
    """
    self.menu2_button_left.hidden = True
    self.menu2_button_right.hidden = True
    self.menu3_button_left.disabled = False
    self.menu3_button_middle.disabled = False
    self.menu3_button_right.disabled = False


def hide_rv(self):
    """Hide RecycleView layout.
    """
    self.rv_layout.size_hint = (0, 0)


def hide_menu2(self):
    """Hide 2 icon menu along with its buttons.
    """
    self.menu2_button_left.hidden = True
    self.menu2_button_right.hidden = True


def show_menu3(self):
    """Show 2 icon menu along with its buttons.
    """
    self.menu3_button_left.disabled = False
    self.menu3_button_middle.disabled = False
    self.menu3_button_right.disabled = False

def show_menu2(self):
    """Show 2 icon menu along with its buttons.
    """
    self.menu2_button_left.disabled = False
    self.menu2_button_right.disabled = False

def menu3_to_rv(self, *args):
    """Hide 3 icon menu, disable its buttons
    and show ReycleView layout instead.
    """
    self.menu3_button_left.hidden = True
    self.menu3_button_middle.hidden = True
    self.menu3_button_right.hidden = True
    self.rv_layout.opacity = OPACITY_FULL
    self.rv_layout.size_hint = (1, 1)


def rv_to_menu3(self, *args):
    """Hide ReycleView layout and show the
    3 icon menu along with its buttons.
    """
    self.menu3_button_left.disabled = False
    self.menu3_button_middle.disabled = False
    self.menu3_button_right.disabled = False
    self.rv_layout.opacity = OPACITY_ZERO
    self.rv_layout.size_hint = (0, 0)


def hide_menu3(self, *args):
    """Hide 3 icon menu along with its buttons.
    """
    self.menu3_button_left.hidden = True
    self.menu3_button_middle.hidden = True
    self.menu3_button_right.hidden = True


def menu3_to_lang_screen(self, *args):
    """Hide 3 icon menu along with its buttons
    and show language dropdown spinner.
    """
    self.menu3_button_left.hidden = True
    self.menu3_button_middle.hidden = True
    self.menu3_button_right.hidden = True
    self.lang_layout.opacity = OPACITY_FULL
    self.lang_spinner.disabled = False


def lang_screen_to_menu3(self, *args):
    """Hide language dropdown spinner and show
    3 icon menu along with its buttons.
    """
    self.menu3_button_left.disabled = False
    self.menu3_button_middle.disabled = False
    self.menu3_button_right.disabled = False
    self.lang_layout.opacity = OPACITY_ZERO
    self.lang_spinner.hidden = True
