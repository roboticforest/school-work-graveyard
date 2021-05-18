from pgl import *  # Eric's Portable Graphics Library.
from button import GButton  # Eric's button component from Project 3.
import filechooser as fc  # Eric's file selector dialog from Project 3.

class ProgramSettings:
    def __init__(self):
        _window_width = 800
        _window_height = 600


def load_program_settings():
    try:
        with open("settings.conf", "rt") as settings_file:
            pass
    except FileNotFoundError as err:




def load_points(filename: str) -> set:
    """
    Loads a set of x,y points from the specified text file.

    Each point should be listed on its own line and be a pair of comma separated integers. Invalid points, whitespace, and
    Python style comments are ignored.

    :param filename: A string specifying the text file to read.
    :return: A standard set of points, excluding any duplicates read from the file.
    """

    points = set()
    try:
        with open(filename, "rt") as input_file:
            line_num = 0
            for raw_input_line in input_file.readlines():
                line_num = line_num + 1  # ++line_num

                # Support python-style line comments
                comment_pos = raw_input_line.find("#")
                if comment_pos != -1:
                    raw_input_line = raw_input_line[:comment_pos]

                # Silently skip blank lines.
                # Must be done after comment filtering, just in case a comment leaves a blank line.
                if raw_input_line.strip() == "":
                    continue

                split_pos = raw_input_line.find(",")
                if split_pos != -1:
                    x = raw_input_line[:split_pos]
                    y = raw_input_line[split_pos + 1:]
                    try:
                        x = int(x)
                        y = int(y)
                        points.add((x, y))
                    except ValueError:
                        # One or both coordinates were not integers or some other typo.
                        # Skip the line and move on, but log the result.
                        print("Skipping line {}. Points must be two integers. Line reads: \"{}\"".format(line_num,
                                                                                                         raw_input_line.strip()))
                else:
                    # Lines should be "int, int" (ignoring whitespace and comments).
                    print("Skipping line {}. No comma separator found. Line reads: \"{}\"".format(line_num,
                                                                                                  raw_input_line.strip()))
    except FileNotFoundError as err:
        print("Could not open file \"{}\".".format(filename))
    return points


def main():
    load_program_settings()

    main_window = GWindow(WIN_WIDTH, WIN_HEIGHT)

    def load_points_button_action():
        points_file = fc.choose_input_file()
        points = load_points(points_file)
        if len(points) == 0:
            print("No points were loaded from {} so there is nothing to draw.".format(points_file))
            return

    load_points_button = GButton("Load Points", load_points_button_action)

    main_window.add(load_points_button, 10, 10)
    main_window.event_loop()


# Main program.
if __name__ == "__main__":
    main()
