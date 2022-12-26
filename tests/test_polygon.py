import cv2
import numpy as np
from polygon import Polygon
import tests.example_polys as example_poly


def test_distance_square() -> None:
    """ Tests the distance from a point to a square. """
    square = example_poly.create_rectangle(100, 100)
    
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
        dist = square.signed_distance(p)
        assert dist == d, f"Expected distance {d}, got {dist}."
        

def test_distance_square_with_hole() -> None:
    """ Tests the distance from a point to a square with a hole. """
    square = example_poly.create_rectangle(100, 100)
    
    # Creates a hole in the top left corner
    hole = example_poly.create_rectangle(50, 50)
    
    # Translates hole 25 to the right and down
    hole.shell =  np.array([p + [25, 25] for p in hole.shell])
    
    square = example_poly.create_hole(square, hole)
    
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
        dist = square.signed_distance(p)
        assert dist == d, f"Expected distance {d}, got {dist}."


def test_distance_donut() -> None:
    """ Tests the distance from a point to a donut. """
    donut = example_poly.create_donut(100, 300, 100)
   
    # Points to calculate distance with 
    points = np.array([
        [0, 300],
        [25, 300],
        [50, 300],
        [75, 300],
        [100, 300],
        [125, 300],
        [150, 300],
        [200, 300],
        [250, 300],
        [300, 300]
    ])

    # Expected distances
    expected_dists = np.array([
        0.,
        25.,
        50.,
        75.,
        100.,
        75.,
        50.,
        0.,
        -50.,
        -100.
    ])
    
    index = 0 
    for p, d in zip(points, expected_dists):
        dist = donut.signed_distance(p)
        assert np.round(dist) == d, f"Expected distance {d}, got {dist}. Index {index}."
        index += 1

def test_get_polygon_key_points() -> None:
    """ Tests the key points of a square. """
    square = example_poly.create_rectangle(100, 100)
    key_points = square._get_bbox()
    
    # Expected key points 
    # [x, y, width, height]
    # cv2 bounding rect always adds 1 more to width and height
    # It doesn't matter much for our use case
    
    expected_key_points = np.array([50, 50, 101, 101])
    
    assert np.all(key_points == expected_key_points), f"Expected key points {expected_key_points}, got {key_points}."
    
    # Test with a circle
    circle = example_poly.create_circle(100, 50)
    key_points = circle._get_bbox()
    
    # Expected key points
    expected_key_points = np.array([100, 100, 201, 200])

    assert np.all(key_points == expected_key_points), f"Expected key points {expected_key_points}, got {key_points}."
