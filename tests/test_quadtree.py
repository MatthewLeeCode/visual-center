from quadtree import Quadtree, find_pole
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
    

def test_find_pole_donut() -> None:
    """ Test the find_pole function """
    donut = example_polys.create_donut(100, 300, 100)
    shell = donut.shell
    holes = donut.holes
    # Find the pole
    pole, distance = find_pole(shell, holes, precision=1)
    # Check the pole
    assert donut.signed_distance(pole.astype(int)) >= 0, f"Expected pole to be inside the shell"
    assert distance >= 99 or distance <= 101, f"Expected distance in range 99-101, got {distance}"


def save_image(filename:str, polygon:Polygon, pole:np.ndarray, distance:float, quadtree:Quadtree=None) -> None:
    """ Saves an image of the polygon and the pole. Use opencv """
    # Find min x and min y
    min_x = np.min(polygon.shell[:, 0]).astype(int)
    min_y = np.min(polygon.shell[:, 1]).astype(int)
    max_x = np.max(polygon.shell[:, 0]).astype(int)
    max_y = np.max(polygon.shell[:, 1]).astype(int)
    
    # Create a transparent image the size of the polygon 
    # Using the polygons width, height, centroid.x and centroid.y
    image = np.zeros((max_y + min_y, max_x + min_x, 4), dtype=np.uint8)

    # Convert shell and holes to uint8  
    polygon.shell = polygon.shell.astype(int)
    polygon.holes = [hole.astype(int) for hole in polygon.holes]
    pole = pole.astype(int)
    
    # Draw the polygon
    cv2.fillPoly(image, [polygon.shell], (255, 255, 255, 255))
    # Draw the holes
    for hole in polygon.holes:
        cv2.fillPoly(image, [hole], (0, 0, 0, 0))
    
    
    
    # Draw small blue circle at the centroid
    cv2.circle(image, (polygon.centroid[0], polygon.centroid[1]), 5, (255, 0, 0, 255), -1)
    
    # Draw small circle at the pole
    cv2.circle(image, (pole[0], pole[1]), 5, (0, 0, 255, 255), -1)
    
    # Draw a non filled circle for the distance
    if distance > 0:
        cv2.circle(image, (pole[0], pole[1]), int(distance), (0, 0, 255, 255), 1)
    
    # Save the image
    cv2.imwrite(filename, image)
    
    # If quadtree is not None, draw the quadtree
    if quadtree is not None:
        quadtree.draw(image)
        
    filename = filename.replace(".png", "_quadtree.png")
    cv2.imwrite(filename, image)
    
    

def test_display_output() -> None:
    """ Saves images of the polygon + poles """
    
    # Save image of square
    square = example_polys.create_rectangle(500, 500)
    pole, distance, tree = find_pole(square.shell, square.holes, precision=1, return_quadtree=True)
    save_image("tests/results/square.png", square, pole, distance, tree)

    # Save image of donut
    donut = example_polys.create_donut(100, 300, 100)
    donut = example_polys.scale(donut, 2)
    pole, distance, tree = find_pole(donut.shell, donut.holes, precision=1, return_quadtree=True)
    save_image("tests/results/donut.png", donut, pole, distance, tree)

    # Save image of irregular polygon
    image = cv2.imread("tests/images/irregular_shape.png")
    # Convert image to black and white
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    irregular = example_polys.create_contour(image)
    irregular = example_polys.scale(irregular, 2)
    pole, distance, tree = find_pole(irregular.shell, irregular.holes, precision=1, return_quadtree=True)
    save_image("tests/results/irregular.png", irregular, pole, distance, tree)
    
    # Save image of circle with square holes
    circle = example_polys.create_circle(500)
    square1 = example_polys.create_rectangle(400, 250)
    # Move square1 to center
    square1 = example_polys.translate(square1, 200, 100)

    square2 = example_polys.create_rectangle(150, 150)
    # Move square2 to bottom right
    square2 = example_polys.translate(square2, 550, 550)

    # Create holes
    circle = example_polys.create_hole(circle, square1)
    circle = example_polys.create_hole(circle, square2)

    pole, distance, tree = find_pole(circle.shell, circle.holes, precision=1, return_quadtree=True)
    save_image("tests/results/circle_hole.png", circle, pole, distance, tree)