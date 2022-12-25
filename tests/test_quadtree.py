from quadtree import Quadtree
import tests.example_polys as example_polys
import numpy as np


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