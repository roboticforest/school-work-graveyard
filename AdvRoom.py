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

MARKER = "-----"


class AdvRoom:

    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new room with the specified attributes."""

    def get_name(self):
        """Returns the name of this room.."""

    def get_short_description(self):
        """Returns a one-line short description of this room.."""

    def get_long_description(self):
        """Returns the list of lines describing this room."""

    def get_next_room(self, verb):
        """Returns the name of the destination room after applying verb."""

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
        :return: None if a room could not be properly read, otherwise an AdvRoom object.
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
        passages = {}
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
                room_exit_verb = line[:split_pos].upper()
                destination_room = line[split_pos + 1:].strip()
                passages[room_exit_verb] = destination_room

        return AdvRoom(name, short_desc, long_desc, passages)
