from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.graphics import Color, Ellipse, ScissorPush, ScissorPop
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty

from Constants import OPACITY_ON, OPACITY_OFF, OPACITY_FULL, OPACITY_ZERO


class TouchRippleButton(TouchRippleBehavior, Button):
    """Dedicated implementation of a Button class with Touch Ripple animation.
    Implements such features as disabling and hiding the button with applying
    opacity changes to its background and other elements depending on its state.
    """
    background_size = ListProperty([0, 0])
    background_offset = ListProperty([0, 0])
    background_image = ObjectProperty()
    background_image_list = ListProperty([])
    disabled = BooleanProperty(False)
    hidden = BooleanProperty(False)
    label = ObjectProperty(None)
    outside_label = ObjectProperty(None)
    icon = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TouchRippleButton, self).__init__(**kwargs)

        # Clear all button's background-related properties
        self.background_normal = ""
        self.background_down = ""
        self.background_disabled_down = ""
        self.background_disabled_normal = ""
        self.background_color = [0, 0, 0, 0]

        self.ripple_duration_in = 0.15
        self.ripple_duration_out = 0.05
        self.ripple_scale = 2.5

    def on_disabled(self, *args):
        """Allows a convenient button disabling.
        If disabled is True the button will not react
        to presses and its background will be partly
        transparent (grayed out).
        """
        # If the button is hidden (this callback gets called
        # on self.hidden since it sets self.disabled) don't
        # modify opacity settings.
        # Although, if button is hidden and self.disabled is
        # set to False, then set self.hidden to False too, to
        # make the button visible and responsive again

        if self.hidden:
            if not self.disabled:
                self.hidden = False
            else:
                pass
        else:
            if self.background_image is not None:
                if self.disabled:
                    self.background_image.opacity = OPACITY_OFF
                else:
                    self.background_image.opacity = OPACITY_ON

            if self.outside_label is not None:
                if self.disabled:
                    self.outside_label.opacity = OPACITY_OFF
                else:
                    self.outside_label.opacity = OPACITY_ON

            elif self.background_image_list is not []:
                if self.disabled:
                    for image in self.background_image_list:
                        image.opacity = OPACITY_OFF
                else:
                    for image in self.background_image_list:
                        image.opacity = OPACITY_ON
            # Maybe an exception could be risen here (because
            # basically nothing will happen without background
            # provided, but on the other hand presses will be
            # blocked anyway, so a "pass" seems to be enough).
            else:
                pass

    def on_hidden(self, *args):
        """Allows a convenient button disabling and hiding
        if its background along with label and icon are
        provided.
        """
        if self.hidden:
            self.disabled = True
            if self.outside_label is not None:
                self.outside_label.opacity = OPACITY_ZERO
            if self.background_image is not None:
                self.background_image.opacity = OPACITY_ZERO
            elif self.background_image_list is not []:
                for image in self.background_image_list:
                    image.opacity = OPACITY_ZERO
            if self.label is not None:
                self.label.opacity = OPACITY_ZERO
            if self.icon is not None:
                self.icon.opacity = OPACITY_ZERO
            self.opacity = OPACITY_ZERO
        else:
            if self.disabled:
                if self.outside_label is not None:
                    self.outside_label.opacity = OPACITY_OFF
                if self.background_image is not None:
                    self.background_image.opacity = OPACITY_OFF
                elif self.background_image_list is not []:
                    for image in self.background_image_list:
                        image.opacity = OPACITY_OFF
                if self.label is not None:
                    self.label.opacity = OPACITY_FULL
                if self.icon is not None:
                    self.icon.opacity = OPACITY_FULL
            else:
                if self.outside_label is not None:
                    self.outside_label.opacity = OPACITY_FULL
                if self.background_image is not None:
                    self.background_image.opacity = OPACITY_FULL
                elif self.background_image_list is not []:
                    for image in self.background_image_list:
                        image.opacity = OPACITY_FULL
                if self.label is not None:
                    self.label.opacity = OPACITY_FULL
                if self.icon is not None:
                    self.icon.opacity = OPACITY_FULL
                self.opacity = OPACITY_FULL

    def on_touch_down(self, touch):
        """Receive a touch down event.

        Args:
            touch (MotionEvent): MotionEvent class touch received.
            The touch is in parent coordinates.
        """
        if self.collide_point(touch.x, touch.y) and not self.disabled:
            touch.grab(self)
            self.ripple_show(touch)
            self.dispatch("on_press")

            # > Uncomment to allow ripple to fade after the
            # > animation is finished. Commenting this snippet
            # > out makes the ripple overlay to stay over
            # > a button as long as it is pressed (but not
            # > outside of its boundaries).
            # def fade(dt):
            #     self.ripple_fade()
            # Clock.schedule_once(fade, self.ripple_duration_out)

            return True
        else:
            return False

    def on_touch_move(self, touch):
        """Receive a moving touch event.

        Args:
            touch (MotionEvent): MotionEvent class touch received.
            The touch is in parent coordinates.
        """
        if not self.collide_point(touch.x, touch.y):
            # If touch is moved out from button's bounding
            # box, then release it and show fading animation.
            touch.ungrab(self)
            self.ripple_fade()
            return False
        else:
            return True

    def on_touch_up(self, touch):
        """Receive a touch up event.

        Args:
            touch (MotionEvent): MotionEvent class touch received.
            The touch is in parent coordinates.
        """
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()

            if self.collide_point(touch.x, touch.y):
                def release(dt):
                    self.dispatch("on_release")

                Clock.schedule_once(release, self.ripple_duration_out)

            return True
        else:
            return False

    def ripple_show(self, touch):
        """Begin ripple animation on current widget.
        Expects touch event as argument. Provided offsets
        are applied to the animation.

        Args:
            touch (MotionEvent): MotionEvent class touch received.
            The touch is in parent coordinates.
        """
        Animation.cancel_all(self, "ripple_rad", "ripple_color")
        self._ripple_reset_pane()
        x, y = self.to_window(*self.pos)
        x += self.background_offset[0]
        y += self.background_offset[1]
        width, height = self.size if self.background_size == [0, 0] else self.background_size
        if isinstance(self, RelativeLayout):
            self.ripple_pos = ripple_pos = (touch.x - x, touch.y - y)
        else:
            self.ripple_pos = ripple_pos = (touch.x, touch.y)
        rc = self.ripple_color
        ripple_rad = self.ripple_rad
        self.ripple_color = [rc[0], rc[1], rc[2], self.ripple_fade_from_alpha]
        with self.ripple_pane:
            ScissorPush(x=int(round(x)), y=int(round(y)), width=int(round(width)), height=int(round(height)))
            self.ripple_col_instruction = Color(rgba=self.ripple_color)
            self.ripple_ellipse = Ellipse(
                size=(ripple_rad, ripple_rad), pos=(ripple_pos[0] - ripple_rad / 2.0, ripple_pos[1] - ripple_rad / 2.0)
            )
            ScissorPop()
        anim = Animation(
            ripple_rad=max(width, height) * self.ripple_scale,
            t=self.ripple_func_in,
            ripple_color=[rc[0], rc[1], rc[2], self.ripple_fade_to_alpha],
            duration=self.ripple_duration_in,
        )
        anim.start(self)

    def ripple_fade(self):
        """Finish ripple animation on current widget.
        """
        Animation.cancel_all(self, "ripple_rad", "ripple_color")
        width, height = self.background_size if self.background_size != [0, 0] else self.size
        rc = self.ripple_color
        duration = self.ripple_duration_out
        anim = Animation(
            ripple_rad=max(width, height) * self.ripple_scale,
            ripple_color=[rc[0], rc[1], rc[2], 0.0],
            t=self.ripple_func_out,
            duration=duration,
        )
        anim.bind(on_complete=self._ripple_anim_complete)
        anim.start(self)

    def unbind_all(self, event_name):
        """Unbinds all events bound to button. They are required
        to be bound with fbind though. Bound by bind function will
        not be unbound by this since they have no UID (it's value
        is None).

        Args:
            event_name (string): Name of event type that the callback
            is bound to (eg. 'on_release').
        """
        for binding in self.get_property_observers(event_name, True):
            self.unbind_uid(event_name, binding[4])
