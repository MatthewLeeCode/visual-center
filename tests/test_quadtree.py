from quadtree import Quadtree, find_pole, find_pole_polygon
import tests.example_polys as example_polys
from polygon import Polygon
import numpy as np
import cv2
import pytest


def test_radius_calculation() -> None:
    """ Test the radius calculation """
    square = example_polys.create_rectangle(10, 10)
    # Create a quadtree
    quadtree = Quadtree(square, 0, 0, 20, 20)
    # Check the radius
    assert round(quadtree.radius, 2) == 14.14, f"Expected 14.14, got {quadtree.radius}"
    
    
def test_cell_max() -> None:
    """ Test the cell max which is the distance to the nearest polygon edge + the radius """
    square = example_polys.create_rectangle(50, 50)
    # Create a quadtree
    quadtree = Quadtree(square, 25, 25, 100, 100)
    # Radius will be 70.71
    # Distance will be 25
    # Max will be 95.71
    # Check the max depth
    assert round(quadtree.cell_max, 2) == 95.71, f"Expected 95.71, got {quadtree.cell_max}"
    
    
def test_find_pole_square() -> None:
    """ Test the find_pole function """
    square = example_polys.create_rectangle(50, 50)
    shell = square.shell
    holes = square.holes
    # Find the pole
    pole, distance = find_pole(shell, holes, precision=1)
    # Check the pole
    assert np.all(pole == np.array([25, 25])), f"Expected [25, 25], got {pole}"
    assert round(distance, 2) == 25, f"Expected 25, got {distance}"
    

def save_image(filename:str, polygon:Polygon, pole:np.ndarray, distance:float) -> None:
    """ Saves an image of the polygon and the pole. Use opencv"""
    # Create a transparent image the size of the polygon
    image = np.zeros((polygon.height, polygon.width, 4), np.uint8)
    # Draw the polygon
    cv2.fillPoly(image, [polygon.shell], (255, 255, 255, 255))
    # Draw the holes
    for hole in polygon.holes:
        cv2.fillPoly(image, [hole], (0, 0, 0, 0))
    
    # Draw small circle at the pole
    cv2.circle(image, (pole[0], pole[1]), 5, (0, 0, 255, 255), -1)
    
    # Draw a non filled circle for the distance
    cv2.circle(image, (pole[0], pole[1]), int(distance), (0, 0, 255, 255), 1)
    
    # Save the image
    cv2.imwrite(filename, image)
    

def test_display_output() -> None:
    """ Saves images of the polygon + poles """
    
    # Save image of square
    square = example_polys.create_rectangle(500, 500)
    pole, distance = find_pole_polygon(square, precision=1)
    save_image("tests/results/square.png", square, pole, distance)
    