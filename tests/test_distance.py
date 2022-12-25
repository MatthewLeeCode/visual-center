import cv2
import numpy as np
from polygon import distance_to_poly
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