"""
This file is used to create example polygons to be used to test.

The following polygons can be created:
- Rectangle
- Circle
- Hexagon

Additionally, any polygon can be used as a hole in any other polygon.
"""
import numpy as np
from polygon import Polygon


def create_rectangle(width: int, height: int) -> Polygon:
    """ Creates a rectangle with the given width and height.

    Args:
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.

    Returns:
        A Polygon of the rectangle.
    """
    return Polygon(np.array([
        [0, 0],
        [width, 0],
        [width, height],
        [0, height]
    ]))
    

def create_circle(radius: int, num_points: int = 100) -> Polygon:
    """ Creates a circle with the given radius.

    Args:
        radius (int): The radius of the circle.
        num_points (int): The number of points to use to approximate the circle.

    Returns:
        A Polygon of the circle.
    """
    # Create a circle with the given radius
    circle = np.zeros((num_points, 2), dtype=np.float32)
    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        circle[i, 0] = radius * np.cos(angle)
        circle[i, 1] = radius * np.sin(angle)
    return Polygon(circle)


def create_hexagon(radius: int) -> Polygon:
    """ Creates a hexagon with the given radius.

    Args:
        radius (int): The radius of the hexagon.

    Returns:
        A Polygon of the hexagon.
    """
    # Create a hexagon with the given radius
    hexagon = np.zeros((6, 2), dtype=np.float32)
    for i in range(6):
        angle = 2 * np.pi * i / 6
        hexagon[i, 0] = radius * np.cos(angle)
        hexagon[i, 1] = radius * np.sin(angle)
    return Polygon(hexagon)


def create_donut(inner_radius: int, outer_radius: int, num_points: int = 100) -> Polygon:
    """ Creates a donut with the given inner and outer radius.

    Args:
        inner_radius (int): The radius of the inner circle.
        outer_radius (int): The radius of the outer circle.
        num_points (int): The number of points to use to approximate the circle.

    Returns:
        np.ndarray: A Polygon of the donut
    """
    return Polygon(create_circle(outer_radius, num_points), [create_circle(inner_radius, num_points)])


def create_concave(num_points: int = 100) -> Polygon:
    """ Creates a concave polygon.

    Args:
        num_points (int): The number of points to use to approximate the polygon.

    Returns:
        A Polygon of the polygon.
    """
    # Create a concave polygon
    concave = np.zeros((num_points, 2), dtype=np.float32)
    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        concave[i, 0] = 100 * np.cos(angle) + 50 * np.cos(5 * angle)
        concave[i, 1] = 100 * np.sin(angle) + 50 * np.sin(5 * angle)
    return Polygon(concave)


def create_hole(polygon: Polygon, hole: Polygon) -> Polygon:
    """ Creates a hole in the given polygon.

    Args:
        polygon (Polygon): The polygon to create the hole in.
        hole (Polygon): The hole to create.

    Returns:
        A Polygon of the polygon with the hole.
    """
    polygon.holes.append(hole.shell)
    return polygon