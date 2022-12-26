"""
This file is used to create example polygons to be used to test.

The following polygons can be created:
- Rectangle
- Circle
- Hexagon

Additionally, any polygon can be used as a hole in any other polygon.
"""
import numpy as np
import cv2
from polygon import Polygon


def translate(polygon: Polygon, x: int, y: int) -> Polygon:
    """ Translates the polygon by the given x and y values.

    Args:
        polygon (Polygon): The polygon to translate.
        x (int): The x value to translate by.
        y (int): The y value to translate by.

    Returns:
        Polygon: The translated polygon.
    """
    # Translate the polygon
    polygon.shell[:, 0] += x
    polygon.shell[:, 1] += y
    for hole in polygon.holes:
        hole[:, 0] += x
        hole[:, 1] += y
        
    polygon._calculate_key_points()
    return polygon


def scale(polygon: Polygon, scale: float) -> Polygon:
    """ Scales the polygon by the given scale.

    Args:
        polygon (Polygon): The polygon to scale.
        scale (float): The scale to scale by.

    Returns:
        Polygon: The scaled polygon.
    """
    # Scale the polygon
    polygon.shell[:, 0] *= scale
    polygon.shell[:, 1] *= scale
    for hole in polygon.holes:
        hole[:, 0] *= scale
        hole[:, 1] *= scale
        
    polygon._calculate_key_points()
    return polygon


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
    
    # Translate to the center
    circle = translate(Polygon(circle), radius, radius)
    return circle


def create_contour(image:np.ndarray) -> Polygon:
    """ Creates a contour from the given image.

    Args:
        image (np.ndarray): The image to create the contour from.

    Returns:
        A Polygon of the contour.
    """
    # Convert to float
    image = image.astype(np.uint8)
    # Find the contour
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour = Polygon(contours[0])
    return contour


def create_donut(inner_radius: int, outer_radius: int, num_points: int = 100) -> Polygon:
    """ Creates a donut with the given inner and outer radius.

    Args:
        inner_radius (int): The radius of the inner circle.
        outer_radius (int): The radius of the outer circle.
        num_points (int): The number of points to use to approximate the circle.

    Returns:
        np.ndarray: A Polygon of the donut
    """
    outer_circle = create_circle(outer_radius, num_points)
    inner_circle = create_circle(inner_radius, num_points)
    # Translate inner circle to center of outer circle
    inner_circle = translate(inner_circle, outer_radius - inner_radius, outer_radius - inner_radius)
    donut = create_hole(outer_circle, inner_circle)
    return donut


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