from pgl import *
import random
import math


def random_color() -> str:
    new_color = "#"
    for i in range(6):
        new_color += random.choice("0123456789ABCDEF")
    return new_color


def set_object_color(pgl_shape_obj: GFillableObject, color: str = None, outline_color: str = None, outline_thickness=1):
    """
    Sets all of the color and outline properties of an object.

    :param pgl_shape_obj: Any drawable PGL object that supports fill colors.
    :param color: Provides the object a fill color, otherwise it is transparent. If this argument is set without also
           setting an outline color, than this will be used as the outline as well since outlines can not be turned off.
    :param outline_color: Specifies the color to use when drawing the outline of the object.
    :param outline_thickness: The thickness of the object outline. Outlines are always drown, so setting this to 0 has no
           affect. However, leaving line thickness at the default of 1 pixel and setting only the color property works to
           draw a shape without an outline.
    :return: Returns nothing, but modifies the passed in PGL object.
    """
    pgl_shape_obj.set_line_width(outline_thickness)  # Trying to set line thickness to 0 doesn't seem to work.
    if color and not outline_color:
        pgl_shape_obj.set_color(color)
        pgl_shape_obj.set_filled(True)
        pgl_shape_obj.set_fill_color(color)
    if outline_color and not color:
        pgl_shape_obj.set_color(outline_color)
    if color and outline_color:
        pgl_shape_obj.set_color(outline_color)
        pgl_shape_obj.set_filled(True)
        pgl_shape_obj.set_fill_color(color)


def make_centered_square(center_x: int, center_y: int, square_size: int, color: str = None, outline_color: str = None,
                         outline_thickness: int = 1) -> GRect:
    """
    Creates a square centered at the given x and y position.

    :param center_x: The x-axis pos the square should be centered around.
    :param center_y: The y-axis pos the square should be centered around.
    :param square_size: The full diameter width (or height) of the square.
    :param color: (optional) The full color of the square if specified alone, otherwise it is the color of the outline around the square.
    :param outline_color: (optional) The color of the square if it should have a different color from its outline.
    :param outline_thickness: (optional) The width of the outline.
    :return: A GRect with equal width and height, centered at the given x and y coordinates.
    """
    square = GRect(center_x - square_size // 2, center_y - square_size // 2, square_size, square_size)

    set_object_color(square, color, outline_color, outline_thickness)

    return square


def make_centered_circle(center_x: int, center_y: int, radius: int, color: str = None, outline_color: str = None,
                         outline_thickness: int = 1) -> GOval:
    """
    Creates a circle centered at the given x and y position.

    :param center_x: The x-axis pos the circle should be centered around.
    :param center_y: The y-axis pos the circle should be centered around.
    :param radius: The distance from the center of the circle to its edge.
    :param color: (optional) The full color of the circle if specified alone, otherwise it is the color of the outline
           around the circle.
    :param outline_color: (optional) The color of the circle if it should have a different color from its outline.
    :param outline_thickness: (optional) The width of the outline.
    :return: A GOval with equal width and height, centered at the given x and y coordinates.
    """
    circle = GOval(center_x - radius, center_y - radius, 2 * radius, 2 * radius)

    set_object_color(circle, color, outline_color, outline_thickness)

    return circle


def make_centered_oval(center_x: int, center_y: int, width: int, height: int, color: str = None, outline_color: str = None,
                       outline_thickness: int = 1) -> GOval:
    """
    Creates an oval centered at the given x and y position.

    :param center_x: The x-axis pos the oval should be centered around.
    :param center_y: The y-axis pos the oval should be centered around.
    :param width: The horizontal diameter of the oval.
    :param height: The vertical diameter of the oval.
    :param color: (optional) The full color of the oval if specified alone, otherwise it is the color of the outline
           around the oval.
    :param outline_color: (optional) The color of the oval if it should have a different color from its outline.
    :param outline_thickness: (optional) The width of the outline.
    :return: A GOval of the given width and height, centered at the given x and y coordinates.
    """
    oval = GOval(center_x - width // 2, center_y - height // 2, width, height)

    set_object_color(oval, color, outline_color, outline_thickness)

    return oval


def center_object_at(pgl_shape_obj: GObject, x: int, y: int):
    pgl_shape_obj.set_location(x - pgl_shape_obj.get_width() // 2, y - pgl_shape_obj.get_height() // 2)


def make_triangle(height: float) -> GPolygon:

    def get_tri_edge_length(tri_height: float):
        return 2 * ((tri_height * math.sqrt(3)) / 3)

    edge_length = get_tri_edge_length(height)

    tri = GPolygon()
    tri.add_vertex(0, -(height / 2))
    tri.add_polar_edge(edge_length, 240)
    tri.add_polar_edge(edge_length, 0.0)

    return tri


# Main program.
if __name__ == "__main__":
    print("PGL Utilities Test")
