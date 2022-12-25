""" Functions for working with polygons."""
import cv2
import numpy as np


def distance_to_poly(point: np.ndarray, shell: np.ndarray, holes:list[np.ndarray]=[]) -> float|None:
    """ Calculates the distance from a point to the polygon edge.
    
    Works for any polygon, including with holes.
    
    Args:
        point (np.ndarray): The point to calculate the distance to.
        shell (np.ndarray): The shell of the polygon. Expects a numpy array of shape (n, 2).
            If the shape is (n, 1, 2), it will be reshaped to (n, 2). This is useful for cv2.findContours.
        holes (list[np.ndarray]): The holes in the polygon.

        
    Returns:
        The minimum distance to the polygon edge, or None if the point is outside the polygon.
    """
    # Ensure point is uint8
    point = point.astype(np.uint8)
    
    # Calculate the distance to the shell
    min_dist = cv2.pointPolygonTest(shell, point, True)
    
    # If dist is negative, the point is outside the polygon
    if min_dist < 0:
        return None
    
    # Check the dist to the holes
    for hole in holes:
        # We need to invert the distance, since we dont want the point inside the hole
        hole_dist = cv2.pointPolygonTest(hole, point, True) * -1
        # If the hole distance is negative, the point is inside the hole (Outside the polygon)
        if hole_dist < 0:
            return None
        # Get the minimum distance
        min_dist = min(min_dist, hole_dist)    

    return min_dist


def get_polygon_key_points(polygon: np.ndarray) -> list[np.ndarray]:
    """ Gets the key points of a polygon.
    
    Key points: x, y (centroid), width, height
    
    Args:
        polygon (np.ndarray): The polygon to get the key points from.
            Holes are not required as they are not used in the calculation
    
    Returns:
        A list of key points. [x(int), y(int), width(int), height(int)]
    """
    # Get the bounding box
    x, y, width, height = cv2.boundingRect(polygon)
    # Get the centroid
    centroid = np.array([x + width/2, y + height/2], dtype=np.uint8)
    # Return the key points
    return [*centroid, width, height] # Width and height are always 1 more for some reason