import cv2


def distance_to_poly(point, shell, holes=[]) -> float|None:
    """ Calculates the distance from a point to the polygon edge.
    
    Works for any polygon, including with holes.
    
    Args:
        point: The point to calculate the distance to.
        shell: The shell of the polygon.
        holes: The holes in the polygon.
        
    Returns:
        The minimum distance to the polygon edge, or None if the point is outside the polygon.
    """
    # Calculate the distance to the shell
    min_dist = cv2.pointPolygonTest(shell, point, True)
    
    # If dist is negative, the point is outside the polygon
    if dist < 0:
        return None
    
    # Check the dist to the holes
    for hole in holes:
        # We need to invert the distance, since we dont want the point inside the hole
        hole_dist = cv2.pointPolygonTest(hole, point, True) * -1
        # If the hole distance is negative, the point is inside the hole (Outside the polygon)
        if hole_dist < 0:
            return None
        # Get the minimum distance
        dist = min(dist, hole_dist)    

    return dist