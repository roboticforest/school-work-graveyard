# File: AdvGame.py

"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# Unless you are implementing extensions, you won't need to add new       #
# public methods (i.e., methods called from other modules), but the       #
# amount of code you need to add is large enough that decomposing it      #
# into helper methods will be essential.                                  #
###########################################################################

from AdvRoom import AdvRoom


class AdvGame:

    def __init__(self, rooms):
        """
        Initializes a new AdvGame with the given rooms for players to navigate.

        :param rooms: The world that makes up the adventure for players to play through.
        """
        self._rooms = rooms

    def get_room(self, name: str):
        """Returns the AdvRoom object with the specified name."""
        return self._rooms[name]

    def run(self):
        """Plays the adventure game stored in this object."""
        cur_room = "START"
        while cur_room != "EXIT":
            room: AdvRoom = self.get_room(cur_room)
            if room.has_been_visited():
                print(room.get_short_description())
            else:
                room.set_visited(True)
                for line in room.get_long_description():
                    print(line)
            user_input = input("> ").strip().upper()
            neighboring_room = room.get_connected_room(user_input)
            if neighboring_room is None:
                print("I don't know how to apply that word here.")
            else:
                cur_room = neighboring_room

    @staticmethod
    def read_adventure(file):
        """
        Reads Room data from the given file object and constructs an Adventure Game.

        :param file: On open file object containing the adventure data.
        :return: A new Adventure Game instance.
        """
        rooms = {}
        finished = False
        while not finished:
            room: AdvRoom = AdvRoom.read_room(file)
            if room is None:
                finished = True
            else:
                name = room.get_name()
                if len(rooms) == 0:
                    rooms["START"] = room
                rooms[name] = room
        return AdvGame(rooms)


# Constants
HELP_TEXT = [
    "Welcome to Adventure!",
    "Somewhere nearby is Colossal Cave, where others have found fortunes in",
    "treasure and gold, though it is rumored that some who enter are never",
    "seen again.  Magic is said to work in the cave.  I will be your eyes",
    "and hands.  Direct me with natural English commands; I don't understand",
    "all of the English language, but I do a pretty good job.",
    "",
    "It's important to remember that cave passages turn a lot, and that",
    "leaving a room to the north does not guarantee entering the next from",
    "the south, although it often works out that way.  You'd best make",
    "yourself a map as you go along.",
    "",
    "Much of my vocabulary describes places and is used to move you there.",
    "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
    "I also know about a number of objects hidden within the cave which you",
    "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
    "To reprint the detailed description of where you are, say LOOK.  If you",
    "want to end your adventure, say QUIT."
]
