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

from AdvObject import AdvObject
from AdvRoom import AdvRoom


class AdvGame:
    """Represents and runs an Adventure style game."""

    def __init__(self, rooms):
        """
        Initializes a new AdvGame with the given rooms for players to navigate.

        :param rooms: The world that makes up the adventure for players to play through.
        """
        self._rooms = rooms
        self._all_objects = {}
        self._player_inventory = set()

    def get_room(self, name: str):
        """Returns the AdvRoom object with the specified name."""
        return self._rooms.get(name)

    def run(self):
        """Plays the adventure game stored in this object."""

        # Place all objects into the game world, if any have been loaded.
        if len(self._all_objects) > 0:
            for item_name in self._all_objects:
                loc = self._all_objects[item_name].get_initial_location()
                if loc != "PLAYER":
                    self._rooms[loc].add_object(item_name)
                else:
                    self._player_inventory.add(item_name)

        def display_room(room: AdvRoom, req_full_desc: bool = False):
            """
            Helper function for printing room descriptions based on if the room has been visited.

            :param room: The room to print the description of.
            :param req_full_desc: Require that the full description of the room and all contained items be printed, even
             if the room has been visited by the player.
            """
            if room.has_been_visited() and not req_full_desc:
                print(room.get_short_description())
            else:
                room.set_visited(True)
                for line in room.get_long_description():
                    print(line)

            # Display any objects that may be in the room.
            room_objects = room.get_contents()
            if len(room_objects) > 0:
                for item in room_objects:
                    print(self._all_objects.get(item))

        playing_game = True
        cur_room: AdvRoom = self.get_room("START")
        display_room(cur_room)
        while playing_game:
            # Capture user input and break into tokens using whitespace.
            user_input = []
            while not user_input:
                user_input = input("> ").upper().split()

            # Check for action verbs.
            command = user_input[0]
            if command == "QUIT":
                playing_game = False
                continue
            elif command == "HELP":
                for line in HELP_TEXT:
                    print(line)
                continue
            elif command == "LOOK":
                display_room(cur_room, req_full_desc=True)
                continue
            elif command == "INVENTORY":
                if len(self._player_inventory) < 1:
                    print("You are empty-handed.")
                else:
                    print("You are carrying:")
                    for item in self._player_inventory:
                        print(" ", self._all_objects[item].get_description())
                continue
            elif command == "DROP":
                if len(user_input) > 1:
                    item = user_input[1]  # For clarity of code.
                    if item in self._player_inventory:
                        self._player_inventory.remove(item)
                        cur_room.add_object(item)
                        print("You set down " + self._all_objects[item].get_description() + ".")
                    else:
                        print("You are not carrying that.")
                else:
                    print("Drop what?")
                continue
            elif command == "TAKE":
                if len(user_input) > 1:
                    item = user_input[1]  # For clarity of code.
                    if item in cur_room.get_contents():
                        cur_room.remove_object(item)
                        self._player_inventory.add(item)
                        print("You pick up " + self._all_objects[item].get_description() + ".")
                    else:
                        print("That is not here.")
                else:
                    print("Take what?")
                continue

            # Check for motion verbs.
            if command == "GO" and len(user_input) > 1:  # Small extension, and an easter egg.
                if user_input[1] == "DENNIS":  # "... Obvious exits are NORTH, SOUTH, and DENNIS."
                    print("YOU ARE THY DUNGEONMAN!")
                    print("Ye arrive at Dennis. He wears a sporty frock coat and a long jimberjam.",
                          "He paces about nervously. Obvious exits are NOT DENNIS.")
                    print("> NOT DENNIS")
                    display_room(cur_room, req_full_desc=True)
                    continue
                command = user_input[1]

            neighboring_room_id = cur_room.get_connected_room_name(command)
            if neighboring_room_id is None:
                # Small extension to project guide.
                # If the command was a movement verb of some sort, print a more appropriate message.
                if command in ["NORTH", "SOUTH", "EAST", "WEST", "IN", "OUT", "UP", "DOWN", "FLY", "XYZZY",
                               "TELEPORT", "TRANSPORT", "ENTER", "LEAVE", "EXIT", "CLIMB", "JUMP", "CRAWL", "GO"]:
                    print("You can't go that way.")
                else:
                    print("I don't know how to apply that word here.")
                continue
            elif neighboring_room_id == "EXIT":
                playing_game = False
                print("GAME OVER!")
            else:
                cur_room = self.get_room(neighboring_room_id)
                display_room(cur_room)

    def read_objects(self, object_file):
        """
        Loads game objects from the given file object into memory. This function must be called before the game is run for
        objects to be place into the game world.

        :param object_file: An open file instance containing the game objects to add to the game world.
        :return: Nothing
        """
        objects = {}
        finished = False
        while not finished:
            game_object: AdvObject = AdvObject.read_object(object_file)
            if game_object is None:
                finished = True
            else:
                objects[game_object.get_name()] = game_object
        self._all_objects = objects

    @staticmethod
    def read_adventure(room_file):
        """
        Reads room description data from the given file object and constructs an Adventure style game.

        :param room_file: An open file object containing the adventure data.
        :return: A new Adventure game instance.
        """
        rooms = {}
        finished = False
        while not finished:
            room: AdvRoom = AdvRoom.read_room(room_file)
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
