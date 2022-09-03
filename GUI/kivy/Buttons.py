from kivy.core.window import Window

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