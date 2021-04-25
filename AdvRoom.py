# File: AdvRoom.py

# REFERENCES:
# I googled "python file type hint" and got:
# https://stackoverflow.com/questions/38569401/type-hint-for-a-file-or-file-like-object
# which linked to:
# https://docs.python.org/3/library/typing.html#typing.IO

"""
This module is responsible for modeling a single room in Adventure.
"""

import typing

from text_utils import ordinal_str

###########################################################################
# Your job in this milestone is to fill in the definitions of the         #
# methods listed in this file, along with any helper methods you need.    #
# The public methods shown in this file are the ones you need for         #
# Milestone #1.  You will need to add other public methods for later      #
# milestones, as described in the handout.  For Milestone #7, you will    #
# need to move the get_next_room method into AdvGame and replace it here  #
# with a get_passages method that returns a dictionary of passages.       #
###########################################################################

# Constants

# Separates the room description and room exit list. Complete sets of room information are separated by a blank line.
MARKER = "-----"


class AdvRoom:
    """Represents an individual room within an Adventure style text game."""

    def __init__(self, name: str, short_desc: str, long_desc: list, room_exits: dict):
        """
        Initializes an Adventure Room object with the specified attributes.

        :param name: The unique ID of the room. This should be a human readable plain text string, like "EndOfRoad".
        :param short_desc: A single line description of the room to display to the player.
        :param long_desc: A list of lines of text to display to the user which describes the appearance of the room they
         are standing within.
        :param room_exits: A dictionary of room exits. Expected is a dict[str, str], where the key is a string representing
         the directional command players will type and the data will be the ID of the room to send the player to.
        """
        self._name = name
        self._short_description = short_desc
        self._long_description = long_desc
        self._exits = room_exits
        self._visited = False
        self._objects = set()

    def add_object(self, obj_name: str):
        """
        Places the named game object within the room.
        
        :param obj_name: The name of the object to add into the room.
        :return: Nothing.
        """
        self._objects.add(obj_name)

    def remove_object(self, name: str):
        """
        Takes the named game object out of the room.

        :param name: The name of the object to remove.
        :return: Nothing.
        """
        self._objects.remove(name)

    def contains_object(self, name: str) -> bool:
        """
        Checks to see if the named game object is contained within the room.

        :param name: The name of the object to search for.
        :return: True if the given name matches the name of an object within the room, False otherwise.
        """
        return name in self._objects

    def get_contents(self) -> set:
        """
        Gets the names of all game objects contained within the room.

        :return: A set listing the names of all objects contained within the room.
        """
        return self._objects.copy()

    def get_name(self) -> str:
        """Returns the name of this room."""
        return self._name

    def get_short_description(self) -> str:
        """Returns a one-line short description of this room."""
        return self._short_description

    def get_long_description(self) -> list:
        """Returns the list of lines describing this room."""
        return self._long_description

    def get_connected_room_name(self, exit_command: str):
        """
        Tries to look up the name of a neighboring room associated with the given room exiting travel command word
        (such as "NORTH", or "IN").

        :param exit_command: A string containing, typically, a travel direction such as "SOUTH" or "OUT".
        :return: The ID of the neighboring connected room, if there is one connected via the given command word.
        """
        return self._exits.get(exit_command)

    def set_visited(self, is_visited: bool):
        """Marks this room as having been visited by the player."""
        self._visited = is_visited

    def has_been_visited(self) -> bool:
        """Checks to see if this room has been visited by the player."""
        return self._visited

    @staticmethod
    def read_room(room_file: typing.TextIO):
        """
        Reads a single room from the given file if possible.

        Room files are plain text, formatted as follows:
          UniqueNameOfRoom
          Short description line.
          Multiline long descriptions that
          can go on and on
          until the marker is read.
          -----
          VERB: RoomName
          VERB: AnotherRoom/ITEM

        :param room_file: An open file object connected to a text file containing room data.
        :return: None if a room could not be properly read (or if EOF is reached), otherwise an AdvRoom object.
        """

        # Setup a small helper to minimize typos, and ensure consistent line counting.
        lines_read = 0  # Count lines for better error messages.

        def get_next_line_from_file():
            """A tiny helper to ensure line counting and whitespace stripping."""
            nonlocal room_file
            nonlocal lines_read
            lines_read += 1
            return room_file.readline().strip()

        # Read in, bare minimum, the room name and short description.
        name = get_next_line_from_file()
        short_desc = get_next_line_from_file()
        if name == "" or short_desc == "":
            return None

        # Read in the long description.
        # The description ends at the MARKER constant.
        done = False
        long_desc = []
        while not done:
            line = get_next_line_from_file()
            if line == MARKER:
                done = True
            else:
                long_desc.append(line)

        # Read in the list of available room changing verbs and destinations.
        # The list end is marked by a blank line.
        done = False
        room_exits = []
        while not done:
            line = room_file.readline().strip()
            if line == "":
                done = True
            else:
                split_pos = line.find(":")
                if split_pos == -1:
                    msg = "Missing colon separator on the {0} line of room {1}. The line reads: \"{2}\"".format(
                        ordinal_str(lines_read), name, line)
                    raise ValueError(msg)
                exit_command = line[:split_pos].upper()
                destination_room = line[split_pos + 1:].strip()
                requirement = None

                # Handle optional room requirement.
                split_pos = destination_room.find("/")
                if split_pos != -1:
                    requirement = destination_room[split_pos + 1:]
                    destination_room = destination_room[:split_pos]

                room_exits.append((exit_command, destination_room, requirement))

        return AdvRoom(name, short_desc, long_desc, room_exits)
