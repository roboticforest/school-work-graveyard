import math

from pgl import *
from pgl_utils import *
from button import GButton
import random

# GWindows can't be resized programmatically, nor does GWindow.get_width() ever return anything other than the window's
# initial value even if the user resizes the window.
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768


class GameSettings:
    def __init__(self):
        self._misses_allowed = 10

    # Combination getter/setter function.
    def misses_allowed(self, new_miss_max=None):
        """
        Getter/setter for how many times a player can miss each round.

        :param new_miss_max: An integer that (if supplied) sets how many times a player can miss before losing.
        :return: The current setting for how many missed clicks a player can make.
        """
        if new_miss_max is not None:
            self._misses_allowed = int(new_miss_max)
        return self._misses_allowed


class GameObject:
    def __init__(self, parent_window: GWindow, start_x, start_y, init_x_vel, init_y_vel):
        self._x = start_x
        self._y = start_y
        self._x_vel = init_x_vel
        self._y_vel = init_y_vel
        self._shape = None
        self._parent_win = parent_window

    def x(self, new_x_pos=None):
        if new_x_pos is not None:
            self._x = float(new_x_pos)
        return self._x

    def y(self, new_y_pos=None):
        if new_y_pos is not None:  # Simply stating "if new_y_pos:" fails when dealing with numbers. A tricky to find bug.
            self._y = float(new_y_pos)
        return self._y

    def x_velocity(self, new_x_vel=None):
        if new_x_vel is not None:
            self._x_vel = float(new_x_vel)
        return self._x_vel

    def y_velocity(self, new_y_vel=None):
        if new_y_vel is not None:
            self._y_vel = float(new_y_vel)
        return self._y_vel

    def visible_shape(self, shape: GFillableObject = None):
        if shape is not None:
            self._parent_win.remove(self._shape)
            self._shape = shape
            self._parent_win.add(self._shape)
        return self._shape

    def update(self):
        pass


class BouncingTarget(GameObject):
    def __init__(self, parent_window: GWindow, speed, color, size):
        GameObject.__init__(self, parent_window, random.randint(0 + size, WINDOW_WIDTH - size),
                            random.randint(0 + size, WINDOW_HEIGHT - size), 0, 0)
        self.visible_shape(make_centered_circle(self.x(), self.y(), size, color, "black", 3))
        split_percent = random.random()
        x_dir = random.choice([1.0, -1.0])
        y_dir = random.choice([1.0, -1.0])
        self.x_velocity(speed * split_percent * x_dir)
        self.y_velocity(speed * (1 - split_percent) * y_dir)

    def update(self):
        self.x(self.x() + self.x_velocity())
        self.y(self.y() + self.y_velocity())

        # Bounds check against the window borders.

        # Right wall check
        if self.x() + self.visible_shape().get_width() // 2 > WINDOW_WIDTH:
            self.x(WINDOW_WIDTH - self.visible_shape().get_width() // 2)
            self.x_velocity(-self.x_velocity())

        # Left wall check
        if self.x() - self.visible_shape().get_width() // 2 < 0:
            self.x(0 + self.visible_shape().get_width() // 2)
            self.x_velocity(-self.x_velocity())

        # Top wall check
        if self.y() - self.visible_shape().get_height() // 2 < 0:
            self.y(0 + self.visible_shape().get_height() // 2)
            self.y_velocity(-self.y_velocity())

        # Bottom wall check
        if self.y() + self.visible_shape().get_height() // 2 > WINDOW_HEIGHT:
            self.y(WINDOW_HEIGHT - self.visible_shape().get_height() // 2)
            self.y_velocity(-self.y_velocity())

        center_object_at(self.visible_shape(), self.x(), self.y())


class SlidingTarget(GameObject):
    def __init__(self, parent_window: GWindow, speed, color, size):
        GameObject.__init__(self, parent_window, random.randint(0, WINDOW_WIDTH), -size, 0, speed)
        self.visible_shape(make_centered_square(self.x(), self.y(), size, color, "black", 3))
        self.y(-self.visible_shape().get_height())

    def update(self):
        self.y(self.y() + self.y_velocity())

        if self.y() - self.visible_shape().get_height() // 2 > WINDOW_HEIGHT:
            self.x(
                random.randint(self.visible_shape().get_width() // 2, WINDOW_WIDTH - self.visible_shape().get_width() // 2))
            self.y(-self.visible_shape().get_height() // 2)

        center_object_at(self.visible_shape(), self.x(), self.y())


def clicker_game():
    main_window = GWindow(WINDOW_WIDTH, WINDOW_HEIGHT)

    def load_game_objects():
        game_objects.append(SlidingTarget(main_window, 1, "blue", 25))
        game_objects.append(SlidingTarget(main_window, 3, "yellow", 25))
        game_objects.append(BouncingTarget(main_window, 1, "blue", 25))
        game_objects.append(BouncingTarget(main_window, 3, "red", 25))

    def update_game():
        if game_state.is_playing:
            for obj in game_objects:
                obj.update()

    def start_button_action():
        # Surrounding if needed to prevent the button from continuing to work after removal from the screen.
        if not game_state.is_playing:
            game_state.is_playing = True
            main_window.remove(start_button)
            load_game_objects()
            main_window.set_interval(update_game, 10)

    background = GRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    set_object_color(background, "darkgray")
    main_window.add(background)

    game_state = GState()
    game_state.is_playing = False
    game_state.game_over = False

    game_objects = []

    start_button = GButton("Start Game", start_button_action)
    center_object_at(start_button, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    main_window.add(start_button)

    # Open the now fully set up window and start the game.
    main_window.event_loop()


# Main program.
if __name__ == "__main__":
    clicker_game()
