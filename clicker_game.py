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
    def __init__(self, parent_window: GWindow, name, start_x, start_y, init_x_vel, init_y_vel):
        self._name = name
        self._x = start_x
        self._y = start_y
        self._x_vel = init_x_vel
        self._y_vel = init_y_vel
        self._shape = None
        self._parent_win = parent_window

    def name(self):
        return self._name

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
            self._shape.object_name = self._name  # Force GObject to have a GameObject name.
            self._parent_win.add(self._shape)
        return self._shape

    def update(self):
        pass


class BouncingTarget(GameObject):
    def __init__(self, parent_window: GWindow, name, speed, color, size):
        GameObject.__init__(self, parent_window, name, random.randint(0 + size, WINDOW_WIDTH - size),
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
    def __init__(self, parent_window: GWindow, name, speed, color, size):
        GameObject.__init__(self, parent_window, name, random.randint(0, WINDOW_WIDTH), -size, 0, speed)
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

    def load_game_objects(level: int = 1) -> bool:
        # Prep for loading the given level.
        game_objects.clear()

        if level == 1:
            # Pretend we're doing this from a file.
            # (kind, speed, color, size, points)
            object_descriptions["blue block"] = ("slider", 1, "blue", 25, 10)
            object_descriptions["yellow block"] = ("slider", 3, "yellow", 25, 30)
            object_descriptions["blue roller"] = ("bouncer", 1, "blue", 25, 5)
            object_descriptions["red ball"] = ("bouncer", 3, "red", 25, 10)
            object_descriptions["lava drip"] = ("slider", 2, "red", 40, 10)

            for obj_name in object_descriptions:
                kind, speed, color, size, _ = object_descriptions[obj_name]
                if kind == "bouncer":
                    game_objects.append(BouncingTarget(main_window, obj_name, speed, color, size))
                if kind == "slider":
                    game_objects.append(SlidingTarget(main_window, obj_name, speed, color, size))

            _, speed, color, size, _ = object_descriptions["blue roller"]
            return True
        if level == 2:
            for i in range(3):
                game_objects.append(SlidingTarget(main_window, "lava drip", 2, "red", 40))
            return True

        return False  # No more levels to load.

    def update_game():
        if game_state.is_playing:
            if game_state.level_complete:
                game_state.current_level = game_state.current_level + 1

                if load_game_objects(game_state.current_level):
                    game_state.level_complete = False
                    game_state.hits = 0
                else:
                    game_state.is_playing = False
                    game_over_label = GLabel("You Win!")
                    main_window.add(game_over_label, WINDOW_WIDTH // 2 - game_over_label.get_width() // 2,
                                    WINDOW_HEIGHT // 2 - game_over_label.get_height() // 2)
                return

            if game_state.game_over:
                game_state.is_playing = False
                game_over_label = GLabel("Game Over")
                main_window.add(game_over_label, WINDOW_WIDTH // 2 - game_over_label.get_width() // 2,
                                WINDOW_HEIGHT // 2 - game_over_label.get_height() // 2)
                return

            for obj in game_objects:
                obj.update()

    def start_button_action():
        # Surrounding if needed to prevent the button from continuing to work after removal from the screen.
        if not game_state.is_playing:
            game_state.is_playing = True
            main_window.remove(start_button)
            load_game_objects()
            game_state.misses_remaining = game_settings.misses_allowed()
            miss_label.set_label("Remaining Attempts: " + str(game_state.misses_remaining))
            main_window.add(miss_label, 10, miss_label.get_height())
            main_window.add(score_label, WINDOW_WIDTH - score_label.get_width() - 10, score_label.get_height())
            main_window.set_interval(update_game, 10)

    def click_action(event: GMouseEvent):
        if game_state.is_playing:
            shape_obj = main_window.get_element_at(event.get_x(), event.get_y())
            if getattr(shape_obj, "object_name", None) is not None:
                game_state.hits = game_state.hits + 1
                main_window.remove(shape_obj)

                _, _, _, _, score = object_descriptions[shape_obj.object_name]
                game_state.player_score = game_state.player_score + score
                score_label.set_label(str(game_state.player_score))
                score_label.set_location(WINDOW_WIDTH - score_label.get_width() - 10, score_label.get_height())
            else:
                game_state.misses_remaining = game_state.misses_remaining - 1
                miss_label.set_label("Remaining Attempts: " + str(game_state.misses_remaining))
            if game_state.misses_remaining <= 0:
                game_state.game_over = True
            if game_state.hits == len(game_objects):
                game_state.level_complete = True

    # Setup the background.
    background = GRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    set_object_color(background, "darkgray")
    main_window.add(background)

    # Load game settings.
    game_settings = GameSettings()

    # Setup game state data.
    game_state = GState()
    game_state.is_playing = False
    game_state.game_over = False
    game_state.level_complete = False
    game_state.misses_remaining = 0
    game_state.player_score = 0
    game_state.hits = 0
    game_state.current_level = 1
    miss_label = GLabel("Remaining Attempts: ")
    score_label = GLabel("0")

    # Setup a place to store game objects.
    object_descriptions = {}
    game_objects = []

    # Setup the game's start button.
    start_button = GButton("Start Game", start_button_action)
    center_object_at(start_button, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    main_window.add(start_button)

    main_window.add_event_listener("mousedown", click_action)

    # Open the now fully set up window and start the game.
    main_window.event_loop()


# Main program.
if __name__ == "__main__":
    clicker_game()
