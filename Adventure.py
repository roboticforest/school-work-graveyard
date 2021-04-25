# File: Adventure.py
# ------------------
# This program plays the CS 151 Adventure game.

from AdvGame import AdvGame

# Constants
DATA_FILE_PREFIX = "Small"


# Main program
def adventure():
    """
    Main Program. Loads and runs an Adventure Game.

    :return: Nothing.
    """
    game = load_adventure_game()
    if game is None:
        print("Failed to load the adventure. Game could not start.")
    else:
        game.run()


def load_adventure_game():
    """
    Loads all Room, Object, and Synonym text files specified by DATA_FILE_PREFIX.

    :return: A new Adventure Game instance.
    """

    adventure_file = DATA_FILE_PREFIX + "Rooms.txt"
    try:
        with open(adventure_file, "rt") as room_file:
            the_adventure = AdvGame.read_adventure(room_file)
    except IOError as err:
        print(err)
        print("Could not load the Adventure Game from file:", adventure_file)
        return None

    try:
        object_filename = DATA_FILE_PREFIX + "Objects.txt"
        with open(object_filename, "rt") as obj_file:
            the_adventure.read_objects(obj_file)
    except IOError as err:
        pass  # Missing object file is not an error.

    try:
        pass
        synonyms_filename = DATA_FILE_PREFIX + "Synonyms.txt"
        with open(synonyms_filename, "rt") as names_file:
            the_adventure.read_synonyms(names_file)
    except IOError as err:
        pass  # Missing synonym file is not an error.

    return the_adventure


# Startup code
if __name__ == "__main__":
    adventure()
