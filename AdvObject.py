# File: AdvObject.js

"""
This module defines a class that models an object in Adventure.
"""

import typing


###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# You won't need to work with this file until Milestone #4.  In my        #
# solution, none of the milestones required any public methods beyond     #
# the ones defined in this starter file.                                  #
###########################################################################

class AdvObject:

    def __init__(self, name: str, description: str, location_room_id: str):
        """Creates an AdvObject from the specified properties."""
        self._name = name
        self._description = description
        self._location = location_room_id

    def __str__(self):
        """Converts an AdvObject to a string."""
        return "There is " + self._description + " here."

    def get_name(self):
        """Returns the name of this object."""
        return self._name

    def get_description(self):
        """Returns the description of this object."""
        return self._description

    def get_initial_location(self):
        """Returns the initial location of this object."""
        return self._location

    @staticmethod
    def read_object(obj_file: typing.TextIO):
        """
        Reads a single object from the given file if possible.

        Object files are plain text, formatted as follows:
          OBJECTNAME
          Short description line.
          RoomIDLocationOfObject

        :param obj_file: An open file object connected to a text file containing object data.
        :return: None if an object could not be properly read, otherwise an AdvObject instance.
        """

        obj_name = ""
        description = ""
        room_id = ""

        done = False
        while not done:

            line = obj_file.readline()
            if line == "":  # If at the end of the file.
                done = True

            obj_name = line.strip().upper()
            if obj_name == "":  # If we read a blank line.
                continue  # read another line.

            # If here, then obj_name has content and the next two lines shouldn't be empty.
            description = obj_file.readline().strip()
            room_id = obj_file.readline().strip().upper()
            done = True

        if obj_name == "" or description == "" or room_id == "":
            return None
        else:
            return AdvObject(obj_name, description, room_id)
