from kivy.core.window import Window
from Constants import (
    BUTTON_CONTENT_SPACING,
    BUTTON_ADDITIONAL_TOUCH_AREA,
    REMOVE_BUTTON_LAYOUT_MAX_WIDTH,
    REMOVE_BUTTON_LAYOUT_BOTTOM_PADDING,
)

# > Button list items (unless otherly specified):
# > button[0] -> button_#_left_end
# > button[1] -> button_#_middle
# > button[2] -> button_#_right_end
# > button[3] -> button_#_icon
# > button[4] -> button_#_label
# > button[5] -> button_#_button


def calculate_button_inner_layout(button_element_array):
    """Calculates and sets up positions and sizes of the
    provided button's elements.

    Args:
        button_element_array (list): List containing button's elements
    """
    left_end = button_element_array[0]
    middle_part = button_element_array[1]
    right_end = button_element_array[2]
    icon = button_element_array[3]
    label = button_element_array[4]
    button = button_element_array[5]

    # Calling texture_update on label to get it's current size
    # label.texture_update()

    left_end.pos = [0, 0]
    middle_part.width = icon.width + BUTTON_CONTENT_SPACING + label.width
    middle_part.pos = [left_end.right, left_end.pos[1]]
    right_end.pos = [middle_part.right, left_end.pos[1]]
    icon.pos = [left_end.right, left_end.pos[1] + (middle_part.height - icon.height) / 2]
    label.pos = [
        icon.right + BUTTON_CONTENT_SPACING,
        left_end.pos[1] + (middle_part.height - label.height) / 2,
    ]
    button.size = [
        left_end.width + middle_part.width + right_end.width + BUTTON_ADDITIONAL_TOUCH_AREA,
        left_end.height + BUTTON_ADDITIONAL_TOUCH_AREA,
    ]
    button.pos = [
        left_end.pos[0] - BUTTON_ADDITIONAL_TOUCH_AREA / 2,
        left_end.pos[1] - BUTTON_ADDITIONAL_TOUCH_AREA / 2,
    ]
    button.background_size = (right_end.right - left_end.pos[0], left_end.height)
    button.background_offset = (BUTTON_ADDITIONAL_TOUCH_AREA / 2, BUTTON_ADDITIONAL_TOUCH_AREA / 2)


def calculate_button_inner_layout_no_icon(button_element_array):
    """Calculates and sets up positions and sizes of the
    provided button's elements.
    This version of the calculate_button_innter_layout takes a button
    that doesn't have an icon. It is used only for setting up "REMOVE"
    button in RecycleViewRow used in consumable lists. In case it is
    needed somewhere else an appropriate changes will have to be made.

    In this case button elements are specified as:
    button_element_array[0] -> button_left_end
    button_element_array[1] -> button_middle
    button_element_array[2] -> button_right_end
    button_element_array[3] -> button_label
    button_element_array[4] -> button_button

    Args:
        button_element_array (list): List containing button's elements
    """

    left_end = button_element_array[0]
    middle_part = button_element_array[1]
    right_end = button_element_array[2]
    label = button_element_array[3]
    button = button_element_array[4]

    # Calling texture_update on label to get it's current size
    # label.texture_update()

    left_end.pos = [0, 0]
    middle_part.width = label.width
    middle_part.pos = [left_end.right, left_end.pos[1]]
    right_end.pos = [middle_part.right, left_end.pos[1]]
    label.pos = [left_end.right, left_end.pos[1] + (middle_part.height - label.height) / 2]
    button_width = left_end.width + middle_part.width + right_end.width
    button.size = [button_width, left_end.height]
    button.background_size = (button_width, left_end.height)

    # Center the button in RecycleView cell
    button_x_offset = (REMOVE_BUTTON_LAYOUT_MAX_WIDTH - button.size[0]) / 2
    for element in button_element_array:
        element.pos[0] += button_x_offset
        element.pos[1] += REMOVE_BUTTON_LAYOUT_BOTTOM_PADDING


def calculate_two_button_layout(button_1, button_2, screen_text):
    """Calculates the layout of two buttons setup (eg. used for choosing if
    user wants to use recycled material or not).

    Args:
        button_1 (list): List containing button_1's elements
        button_2 (list): List containing button_2's elements
        screen_text (Label): Label with text that is displayed on that screen
    """
    if screen_text.parent.height == 360:
        bottom_panel_offset = 96
    else:
        bottom_panel_offset = 192

    screen_half = Window.width / 2
    button_1_width = button_1[0].pos[0] + button_1[2].right
    button_2_width = button_2[0].pos[0] + button_2[2].right

    # What if any of the buttons is too wide?
    # if button_1_width >= half_of_the_screen_width or button_2_width >= half_of_the_screen_width:
    #     pass

    button_1_x_offset = Window.width / 3 - button_1_width / 2
    button_2_x_offset = Window.width * 2 / 3 - button_2_width / 2
    buttons_y_offset = (
        (screen_text.parent.height - screen_text.height) / 3 - button_1[0].height / 2 + bottom_panel_offset
    )

    for element in button_1:
        element.pos[0] += button_1_x_offset
        element.pos[1] += buttons_y_offset

    for element in button_2:
        element.pos[0] += button_2_x_offset
        element.pos[1] += buttons_y_offset

    # Check if buttons are not overlapping or if they aren't too close.
    # If it is so, then set them apart by 40 px.
    overlapping_distance = button_2[0].pos[0] - button_1[2].right

    if overlapping_distance < 40:
        for element in button_1:
            element.pos[0] += screen_half - button_1_width - 20 - button_1_x_offset
        for element in button_2:
            element.pos[0] += screen_half + 20 - button_2_x_offset
    else:
        pass


def calculate_two_button_layout_tab(button_1, button_2, tab_manager):
    """Sets up positions of the provided buttons in provided
    TabbedPopupManager window.

    Args:
        button_1 (list): List containing left (1st) button's elements
        button_2 (list): List containing right (2nd) button's elements
        tab_manager (ModalView): TabbedPopupManager instance which holds the buttons provided
    """
    button_1[5].size[0] -= BUTTON_ADDITIONAL_TOUCH_AREA / 4
    button_2[5].size[0] -= BUTTON_ADDITIONAL_TOUCH_AREA / 4
    button_2[5].pos[0] += BUTTON_ADDITIONAL_TOUCH_AREA / 4
    button_2[5].background_offset[0] -= BUTTON_ADDITIONAL_TOUCH_AREA / 4

    # > The lines below fix a situation when tab_manager.right returns value 904 at the beginning,
    # > but later then it returns 964, which makes sense, since it takes into account the
    # > proper positioning of the ModalView layout in the center of the window.
    # > Since it doesn't account for the positioning at first call, below fix was added
    # > to fix the positioning of the buttons, which rely on tab_manager.right.
    # > If it happens that a better way of fixing that is found, this hacky fix should
    # > be removed.

    if tab_manager.right == 904:
        fix = 60
    else:
        fix = 0

    button_1_x_offset = (
        tab_manager.right - button_2[5].size[0] - button_1[5].size[0] - BUTTON_ADDITIONAL_TOUCH_AREA / 4 + fix
    )
    button_2_x_offset = tab_manager.right - button_2[5].size[0] - BUTTON_ADDITIONAL_TOUCH_AREA / 2 + fix
    buttons_y_offset = -168

    for element in button_1:
        element.pos[0] += button_1_x_offset
        element.pos[1] += buttons_y_offset

    for element in button_2:
        element.pos[0] += button_2_x_offset
        element.pos[1] += buttons_y_offset


def calculate_one_button_layout(button, screen_text):
    """Positions a single button on the screen. Used eg. for starting a process.

    Args:
        button (list): List containing button's elements
        screen_text (Label): Label with text that is displayed on that screen
    """
    if screen_text.parent.height == 360:
        bottom_panel_offset = 96
    else:
        bottom_panel_offset = 192

    button_width = button[0].pos[0] + button[2].right
    button_x_offset = Window.width * 2 / 3 - button_width / 2
    button_y_offset = (screen_text.parent.height - screen_text.height) / 3 - button[0].height / 2 + bottom_panel_offset

    for element in button:
        element.pos[0] += button_x_offset
        element.pos[1] += button_y_offset


def calculate_recycled_material_buttons_layout(layout, screen_text):
    """Used to calculate layout of the buttons which are used to choose the
    amount of recycled material to be used for a casting process.

    Args:
        layout (GridLayout): Buttons' layout
        screen_text (Label): Label with text that is displayed on that screen
    """
    # screen_text.texture_update()
    layout.pos = screen_text.parent.pos
    layout.height = screen_text.parent.height - screen_text.height
    layout.width = screen_text.parent.width


def calculate_nav_buttons(back_button_label, back_button_background, next_button_label, next_button_background):
    """Takes care of positioning the navigation buttons' labels over their
    backgrounds.

    Args:
        back_button_label (Label): Back or exit button label
        back_button_background (Image): Back or exit button background
        next_button_label (Label): Next button label
        next_button_background (Image): Next button background
    """
    min_width = 80
    max_width = 90

    # back_button_label.texture_update()
    # next_button_label.texture_update()

    if back_button_label.width > max_width:
        while back_button_label.width > max_width:
            back_button_label.font_size -= 1
            # back_button_label.texture_update()
    elif back_button_label.width < min_width:
        while back_button_label.width < min_width:
            back_button_label.font_size += 1
            # back_button_label.texture_update()

    if next_button_label.width > max_width:
        while next_button_label.width > max_width:
            next_button_label.font_size -= 1
            # next_button_label.texture_update()
    elif next_button_label.width < min_width:
        while next_button_label.width < min_width:
            next_button_label.font_size += 1
            # next_button_label.texture_update()

    if back_button_label.font_size < next_button_label.font_size:
        next_button_label.font_size = back_button_label.font_size
        # next_button_label.texture_update()
    else:
        back_button_label.font_size = next_button_label.font_size
        # back_button_label.texture_update()

    back_button_label.pos = (
        back_button_background.pos[0]
        + (back_button_background.width - back_button_label.width) / 2
        + 4,  # additional 4 px (dp) margin for better looks
        back_button_background.pos[1] + (back_button_background.height - back_button_label.height) / 2,
    )
    next_button_label.pos = (
        next_button_background.pos[0]
        + (next_button_background.width - next_button_label.width) / 2
        - 4,  # additional -4 px (dp) margin for better looks
        next_button_background.pos[1] + (next_button_background.height - next_button_label.height) / 2,
    )


def calculate_menu3_buttons_fonts(label_left, label_middle, label_right):
    """Adapts font sizes of labels used in 3 element menu to not exceed the
    width of menu icons.

    Args:
        label_left ([type]): Left menu item label
        label_middle ([type]): Center menu item label
        label_right ([type]): Right menu item label
    """
    # Start with default font size (prevents fonts from staying small)
    label_left.font_size = 36
    label_middle.font_size = 36
    label_right.font_size = 36

    # Update textures to apply changes
    # label_left.texture_update()
    # label_middle.texture_update()
    # label_right.texture_update()

    # Perform calculations basing on the widths of respective buttons
    if label_left.texture_size[0] > label_left.parent.width:
        while label_left.texture_size[0] > label_left.parent.width:
            label_left.font_size -= 1
            # label_left.texture_update()

    if label_middle.texture_size[0] > label_middle.parent.width:
        while label_middle.texture_size[0] > label_middle.parent.width:
            label_middle.font_size -= 1
            # label_middle.texture_update()

    if label_right.texture_size[0] > label_right.parent.width:
        while label_right.texture_size[0] > label_right.parent.width:
            label_right.font_size -= 1
            # label_right.texture_update()

    # Set font sizes
    font_size = min(label_left.font_size, label_middle.font_size, label_right.font_size)
    label_left.font_size = font_size
    label_middle.font_size = font_size
    label_right.font_size = font_size

    # Update textures
    # label_left.texture_update()
    # label_middle.texture_update()
    # label_right.texture_update()


def bind_callback(button_element_array, callback, event_name="on_release"):
    """Wraps up binding callbacks to buttons made of multiple elements
    (with adaptive width). By default binds as 'on_release', since it is
    basically the only type of event used in this app.

    Args:
        button_element_array (list): List containing button's elements
        callback (function): Function we want to bind to provided button
        event_name (str, optional): Name of event we want the callback
        to be called. Defaults to 'on_release'.
    """
    try:
        # Normal button
        if len(button_element_array) == 6:
            button = button_element_array[5]
        # Button without icon
        elif len(button_element_array) == 5:
            button = button_element_array[4]
        else:
            return
    # In case a button (touch area) itself is passed
    except TypeError:
        button = button_element_array

    button.fbind(event_name, callback)


def unbind_all_callbacks(button_element_array, event_name="on_release"):
    """Clears all callbacks bound to provided button.

    Args:
        button_element_array (list): List containing button's elements
        event_name (str, optional): Name of event to unbind. Defaults to 'on_release'.
    """
    try:
        # Normal button
        if len(button_element_array) == 6:
            button = button_element_array[5]
        # Button without icon
        elif len(button_element_array) == 5:
            button = button_element_array[4]
        else:
            return
    # In case a button (touch area) itself is passed
    except TypeError:
        button = button_element_array

    button.unbind_all(event_name)
