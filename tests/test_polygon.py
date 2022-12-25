import cv2
import numpy as np
from polygon import distance_to_poly, get_polygon_key_points
import tests.example_polys as poly


def test_distance_square() -> None:
    """ Tests the distance from a point to a square. """
    square = poly.create_rectangle(100, 100)
    
    # Points to calculate distance with
    points = np.array([
        [0, 0],
        [25, 25],
        [50, 50],
        [75, 75],
        [100, 100],
        [150, 150]
    ])
    
    # Expected distances
    expected_dists = np.array([
        0.,
        25.,
        50.,
        25.,
        0.,
        None
    ])
    
    for p, d in zip(points, expected_dists):
        dist = distance_to_poly(p, square)
        assert dist == d, f"Expected distance {d}, got {dist}."
        

def test_get_polygon_key_points() -> None:
    """ Tests the key points of a square. """
    square = poly.create_rectangle(100, 100)
    key_points = get_polygon_key_points(square)
    
    # Expected key points 
    # [x, y, width, height]
    # cv2 bounding rect always adds 1 more to width and height
    # It doesn't matter much for our use case
    
    expected_key_points = np.array([50, 50, 101, 101])
    
    assert np.all(key_points == expected_key_points), f"Expected key points {expected_key_points}, got {key_points}."
    
    # Test with a circle
    circle = poly.create_circle(100, 50)
    key_points = get_polygon_key_points(circle)
    
    # Expected key points
    expected_key_points = np.array([0, 0, 201, 200])

    assert np.all(key_points == expected_key_points), f"Expected key points {expected_key_points}, got {key_points}."
