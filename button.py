# File: button.py

"""
This file defines the GButton class, which implements a simple onscreen
button.
"""

from pgl import GCompound, GRect, GLabel, GWindow

# Class: GButton

class GButton(GCompound):

    """
    This class implements a simple onscreen button consisting of a
    GCompound with a GRect and a GLabel.  Each button is associated
    with a callback function that is called automatically when the
    button is clicked.
    """

# Constants

    BUTTON_FONT = "14px 'Lucida Grande','Helvetica Neue','Sans-Serif'"
    BUTTON_MARGIN = 10
    BUTTON_MIN_WIDTH = 125
    BUTTON_DEFAULT_HEIGHT = 20
    BUTTON_ASCENT_DELTA = -1

# Constructor: GButton

    def __init__(self, text, fn=None):
        GCompound.__init__(self)
        label = GLabel(text)
        # label.set_font(self.BUTTON_FONT)
        width = max(self.BUTTON_MIN_WIDTH,
                    2 * self.BUTTON_MARGIN + label.get_width())
        frame = GRect(width, self.BUTTON_DEFAULT_HEIGHT)
        frame.set_filled(True)
        frame.set_fill_color("White")
        self.add(frame)
        self.add(label)
        self.text = text
        self.label = label
        self.frame = frame
        self.fn = fn
        self._recenter()

# Public method: set_size

    def set_size(self, width, height):
        """
        Sets the dimensions of the button.
        """
        self.frame.set_size(width, height)
        self._recenter()

# Public method: set_font

    def set_font(self, font):
        """
        Sets the font for the button.
        """
        self.label.set_font(font)
        self._recenter()

# Public method: get_font

    def get_font(self):
        """
        Returns the font for the button.
        """
        return self.label.get_font()

# Public method: set_label

    def set_label(self, label):
        """
        Sets the label for the button.
        """
        self.label.set_label(label)
        self._recenter()

# Public method: get_label

    def get_label(self):
        """
        Returns the label for the button.
        """
        return self.label.get_label()

    def __str__(self):
        return "<Button " + self.text + ">"

# Override method: _install

    def _install(self, target, ctm):
        GCompound._install(self, target, ctm)
        if isinstance(target, GWindow):
            target.add_event_listener("click", self._click_action)

# Private method: _click_action

    def _click_action(self, e):
        if self.contains(e.get_x(), e.get_y()):
            self.fn()

# Private method: _recenter

    def _recenter(self):
        x = (self.frame.get_width() - self.label.get_width()) / 2
        y = (self.frame.get_height() + self.label.get_ascent()) / 2
        self.label.set_location(x, y + self.BUTTON_ASCENT_DELTA)

