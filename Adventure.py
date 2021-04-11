# File: Adventure.py
# ------------------
# This program plays the CS 151 Adventure game.

from AdvGame import AdvGame

# Constants
DATA_FILE_PREFIX = "Tiny"


# Main program
def adventure():
    """
    Main Program. Loads and runs an Adventure Game.

    :return: Nothing.
    """
    game = load_adventure_game()
    game.run()


def load_adventure_game():
    """
    Loads all Room, Object, and Synonym text files specified by DATA_FILE_PREFIX.

    :return: A new Adventure Game instance.
    """
    try:
        adventure_file = DATA_FILE_PREFIX + "Rooms.txt"
        with open(adventure_file) as room_file:
            return AdvGame.read_adventure(room_file)
    except IOError as err:
        print("Could not load the Adventure Game from file:", adventure_file)
        print(err)


# Startup code
if __name__ == "__main__":
    adventure()
