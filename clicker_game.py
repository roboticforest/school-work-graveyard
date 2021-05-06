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
    """
    A class for storing the global settings of this particular game.

    Every setting has a default value in case one isn't supplied in a settings
    file, and all settings can be changed at any time.
    """

    def __init__(self):
        """Initializes the game settings with default values."""
        self._misses_allowed = 10

    def load_settings(self, filename):
        """
        Attempts to load all known settings from a file. If any setting is not
        found, or if the setting could not be parsed properly, then the default
        value is used.

        Each setting should be listed on its own line as a simple key=value pairing.

        :param filename: The name of the file that the settings can be found in.
        :return: Nothing.
        """

        try:
            with open(filename, "rt") as settings_file:
                for line in settings_file.readlines():

                    # Support python-style line comments.
                    # This needs to happen before blank line filtering.
                    comment_pos = line.find("#")
                    if comment_pos != -1:
                        line = line[:comment_pos]

                    # Validate lines and check for blanks.
                    split_pos = line.find("=")
                    if line.strip() == "" or split_pos == -1:
                        continue  # Skip blank or invalid lines.

                    # Line should be in valid form. Attempt to parse settings.
                    setting_name = line[:split_pos].strip().upper()
                    setting_value = line[split_pos + 1:].strip()
                    try:
                        if setting_name == "MISSES_ALLOWED":
                            setting_value = int(setting_value)
                            self._misses_allowed = setting_value
                        # FUTURE SETTINGS GO HERE
                        # Level complete awards
                        # Increase amount for misses
                        # Bonus points for finishing a level.
                    except ValueError:
                        continue
        except FileNotFoundError:
            return

    # Combination getter/setter function.
    def misses_allowed(self, new_miss_max=None):
        """
        Getter/setter for how many times a player can miss each round.

        :param new_miss_max: An integer that (if supplied) sets how many times a player can miss before losing.
        :return: The current (or newly set) missed clicks setting.
        """
        if new_miss_max is not None:
            self._misses_allowed = int(new_miss_max)
        return self._misses_allowed


class GameObject:
    """
    Abstract base class (if that term even applies in Python) for all the floating shapes that will move around the screen.

    This class is essentially a wrapper around the GFillableObject class, expanding its abilities for the purposes of this
    'click on the shape' game.
    """

    def __init__(self, parent_window: GWindow, name, start_x, start_y, init_x_vel, init_y_vel):
        """
        Initialized the GameObject with basic data about its position and direction of motion.
        GameObjects add themselves to a parent window.
        """

        self._name = name
        self._x = start_x
        self._y = start_y
        self._x_vel = init_x_vel
        self._y_vel = init_y_vel
        self._shape = None
        self._parent_win = parent_window

    def name(self):
        """
        Get the name of the object. This is read only and names can only be set during object creation.

        Names must be unique and match those found in the object descriptions dictionary used to make GameObjects.
        """
        return self._name

    def x(self, new_x_pos=None):
        """Combination getter/setter for the x-axis position of the object."""
        if new_x_pos is not None:
            self._x = float(new_x_pos)
        return self._x

    def y(self, new_y_pos=None):
        """Combination getter/setter for the y-axis position of the object."""
        if new_y_pos is not None:  # Simply stating "if new_y_pos:" fails when dealing with numbers. A tricky to find bug.
            self._y = float(new_y_pos)
        return self._y

    def x_velocity(self, new_x_vel=None):
        """Combination getter/setter for the x-axis velocity of the object."""
        if new_x_vel is not None:
            self._x_vel = float(new_x_vel)
        return self._x_vel

    def y_velocity(self, new_y_vel=None):
        """Combination getter/setter for the y-axis velocity of the object."""
        if new_y_vel is not None:
            self._y_vel = float(new_y_vel)
        return self._y_vel

    def visible_shape(self, shape: GFillableObject = None):
        """
        Combination getter/setter for defining the actual shape that will be visible to the player within the main window.

        Base GameObjects do not initially create a shape or draw anything to the screen. It is up to implementations of
        classes derived from GameObject to create and manipulate their particular shape objects and then to use this function
        to add those shapes to the window.
        """
        if shape is not None:
            self._parent_win.remove(self._shape)
            self._shape = shape
            self._shape.object_name = self._name  # Force GObject to have a GameObject name.
            self._parent_win.add(self._shape)
        return self._shape

    def update(self):
        """For derived classes to use to create custom behavior. Base GameObjects don't do anything."""
        pass


class BouncingTarget(GameObject):
    """A bouncing ball object that flies around the screen bouncing off of each wall."""

    def __init__(self, parent_window: GWindow, name, speed, color, size):
        """
        Initializes the ball.

        :param parent_window: The window the ball should add itself to.
        :param name: The unique ID of this ball.
        :param speed: The distance (in pixels) the ball will travel each update.
        :param color: A string specifying the color of the ball.
        :param size: The radius of the ball.
        """

        # Initialize the parent object.
        GameObject.__init__(self, parent_window, name, random.randint(0 + size, WINDOW_WIDTH - size),
                            random.randint(0 + size, WINDOW_HEIGHT - size), 0, 0)

        # Define our shape.
        self.visible_shape(make_centered_circle(self.x(), self.y(), size, color, "black", 3))

        # Split the given speed into separate x,y velocities. Randomize the direction for variety.
        split_percent = random.random()
        x_dir = random.choice([1.0, -1.0])
        y_dir = random.choice([1.0, -1.0])
        self.x_velocity(speed * split_percent * x_dir)
        self.y_velocity(speed * (1 - split_percent) * y_dir)

    def update(self):
        """Move the ball around the screen, bouncing off of the edges. Like the ball in pong or breakout."""

        # Move the ball.
        self.x(self.x() + self.x_velocity())
        self.y(self.y() + self.y_velocity())

        # Bounds check the motion against the window borders, reversing the appropriate velocities when needed.

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

        # Finally, move the visible shape to match the position of this object.
        center_object_at(self.visible_shape(), self.x(), self.y())


class SlidingTarget(GameObject):
    """A block which slides across the screen."""

    def __init__(self, parent_window: GWindow, name, speed, color, size):
        """
        Initializes the block.

        :param parent_window: The window the block should add itself to.
        :param name: The unique ID of this block.
        :param speed: The distance (in pixels) the block will travel each update.
        :param color: A string specifying the color of the block.
        :param size: The width/height of the square block.
        """

        # Initialize the parent object.
        GameObject.__init__(self, parent_window, name, random.randint(0, WINDOW_WIDTH), -size, 0, speed)

        # Create the visible shape the player will see.
        self.visible_shape(make_centered_square(self.x(), self.y(), size, color, "black", 3))

        # Set the initial position of the block off the top of the screen.
        self.y(-self.visible_shape().get_height())

    def update(self):
        """Slide the block down the screen."""

        # FUTURE MOVEMENT
        # Slide the block across the screen from side to side, or from bottom to top.

        # Move the block.
        self.y(self.y() + self.y_velocity())

        # Bounds check,
        # if the block moves off the bottom of the screen, reset it to a random position above the screen.
        if self.y() - self.visible_shape().get_height() // 2 > WINDOW_HEIGHT:
            self.x(
                random.randint(self.visible_shape().get_width() // 2, WINDOW_WIDTH - self.visible_shape().get_width() // 2))
            self.y(-self.visible_shape().get_height() // 2)

        # Move the visible GObject to match the final position of this block object.
        center_object_at(self.visible_shape(), self.x(), self.y())


def clicker_game():
    """
    A simple game where you gave to click on the shapes to remove them from the screen.

    Apparently, it's similar to a phone app called Ant Squisher... I didn't know this was a thing.
    """

    # Create the main window.
    main_window = GWindow(WINDOW_WIDTH, WINDOW_HEIGHT)

    # Define helper functions needed by this game.
    # They're defined here instead of at file scope due to their specificity and use of the main_window.

    def load_game_objects(level: int = 1) -> bool:
        """Load all game object descriptions and create specific instances for the given level."""

        # Prep for loading the given level.
        # Clear any game object instances that may have existed from a previous level.
        game_objects.clear()

        # TEMP CODE
        # Pretend to load a bunch of descriptions from a file.
        # Use those descriptions to instantiate a few objects for a couple of levels.
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
        """Updates all game objects and controls global game flow."""

        # Do nothing if the game is not running.
        if game_state.is_playing:

            # If the current level is complete,
            if game_state.level_complete:
                # try to advance to the next level.
                game_state.current_level = game_state.current_level + 1

                # If there is a next level, play it, otherwise the player must have won.
                if load_game_objects(game_state.current_level):
                    game_state.level_complete = False
                    game_state.hits = 0
                else:
                    game_state.is_playing = False
                    game_over_label = GLabel("You Win!")
                    main_window.add(game_over_label, WINDOW_WIDTH // 2 - game_over_label.get_width() // 2,
                                    WINDOW_HEIGHT // 2 - game_over_label.get_height() // 2)
                return

            # If the player lost, end the game.
            if game_state.game_over:
                game_state.is_playing = False
                game_over_label = GLabel("Game Over")
                main_window.add(game_over_label, WINDOW_WIDTH // 2 - game_over_label.get_width() // 2,
                                WINDOW_HEIGHT // 2 - game_over_label.get_height() // 2)
                return

            # If the game isn't ending for some reason, then keep playing.
            # Tell each game object to continue moving around the screen.
            for obj in game_objects:
                obj.update()

    def start_button_action():
        """Removes the start button from the screen and begins the game."""

        # Surrounding if statement is needed here to prevent the button from continuing to function
        # after being removed from the screen. The now invisible button re-adds labels and callback
        # functions if it gets clicked again, causing objects to speed up.
        if not game_state.is_playing:
            game_state.is_playing = True  # Start the game.
            main_window.remove(start_button)  # Remove the start button.
            load_game_objects()  # Load every object the player will attack with their mouse.

            # Setup the misses label.
            game_state.misses_remaining = game_settings.misses_allowed()
            miss_label.set_label("Remaining Attempts: " + str(game_state.misses_remaining))
            main_window.add(miss_label, 10, miss_label.get_height())

            # Setup the player score label.
            main_window.add(score_label, WINDOW_WIDTH - score_label.get_width() - 10, score_label.get_height())

            # Start the game's update loop.
            main_window.set_interval(update_game, 10)

    def click_action(event: GMouseEvent):
        """Respond to the player's mouse clicks."""

        # If the game isn't running, do nothing.
        if game_state.is_playing:

            # Get the GObject the player clicked on.
            shape_obj = main_window.get_element_at(event.get_x(), event.get_y())

            # If GameObject forced it to have a name attribute, then it's a target
            # for the player to click on, otherwise it's something else like a background
            # element or part of the UI.
            if getattr(shape_obj, "object_name", None) is not None:
                game_state.hits = game_state.hits + 1
                main_window.remove(shape_obj)

                # Look up how many points this object is worth and apply that to the player's score.
                _, _, _, _, score = object_descriptions[shape_obj.object_name]
                game_state.player_score = game_state.player_score + score
                score_label.set_label(str(game_state.player_score))
                score_label.set_location(WINDOW_WIDTH - score_label.get_width() - 10, score_label.get_height())
            else:
                game_state.misses_remaining = game_state.misses_remaining - 1
                miss_label.set_label("Remaining Attempts: " + str(game_state.misses_remaining))

            # Check to see if the level should end.
            if game_state.misses_remaining <= 0:  # Check for Game Over!
                game_state.game_over = True
            if game_state.hits == len(game_objects):  # Check for Level Complete!
                game_state.level_complete = True

    # Now that helper functions are all defined...
    # Define game variables and default values.

    # Setup the background.
    background = GRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    set_object_color(background, "darkgray")
    main_window.add(background)

    # Load game settings.
    game_settings = GameSettings()
    game_settings.load_settings("settings.conf")

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

    # Setup event listeners.
    main_window.add_event_listener("mousedown", click_action)

    # Lastly, open the now fully set up window and start the game.
    main_window.event_loop()


# Main program.
if __name__ == "__main__":
    clicker_game()
