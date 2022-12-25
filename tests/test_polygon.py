import cv2
import numpy as np
from polygon import signed_distance, get_polygon_key_points
import tests.example_polys as poly


def test_distance_square() -> None:
    """ Tests the distance from a point to a square. """
    square = poly.create_rectangle(100, 100)
    
    # Points to calculate distance with
    points = np.array([
        [0, 50],
        [25, 50],
        [50, 50],
        [75, 50],
        [100, 50],
        [125, 50],
        [150, 50]
    ])
    
    # Expected distances
    expected_dists = np.array([
        0.,
        25.,
        50.,
        25.,
        0.,
        -25,
        -50
    ])
    
    for p, d in zip(points, expected_dists):
        dist = signed_distance(p, square)
        assert dist == d, f"Expected distance {d}, got {dist}."
        

def test_distance_square_with_hole() -> None:
    """ Tests the distance from a point to a square with a hole. """
    square = poly.create_rectangle(100, 100)
    
    # Creates a hole in the top left corner
    hole = poly.create_rectangle(50, 50)
    
    # Translates hole 25 to the right and down
    hole =  np.array([p + [25, 25] for p in hole])
    
    # Points to calculate distance with
    points = np.array([
        [0, 50],
        [25, 50],
        [50, 50],
        [75, 50],
        [100, 50],
        [125, 50],
        [150, 50]
    ])
    
    # Expected distances
    expected_dists = np.array([
        0.,
        0., # Border of the hole
        -25., # Inside the hole
        0., # Border of the hole
        0., # Border of the square
        -25,
        -50
    ])
    
    for p, d in zip(points, expected_dists):
        dist = signed_distance(p, square, holes=[hole])
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
