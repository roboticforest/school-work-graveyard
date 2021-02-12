# File: AdvObject.js

"""
This module defines a class that models an object in Adventure.
"""

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# You won't need to work with this file until Milestone #4.  In my        #
# solution, none of the milestones required any public methods beyond     #
# the ones defined in this starter file.                                  #
###########################################################################

class AdvObject:

    def __init__(self, name, description, location):
        """Creates an AdvObject from the specified properties."""

    def __str__(self):
        """Converts an AdvObject to a string."""

    def get_name(self):
        """Returns the name of this object."""

    def get_description(self):
        """Returns the description of this object."""

    def get_initial_location(self):
        """Returns the initial location of this object."""

    @staticmethod
    def read_object(f):
        """Reads and returns the next object from the file."""
