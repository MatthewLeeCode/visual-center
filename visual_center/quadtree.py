""" 
Approximating (Really close approximation) of the visual center / pole of inaccessability / largest inscribed circle / point that is furthest from the edge of a polygon 
using a quadtree. 

Implementation completely based off of the polylabel implementation: blog.mapbox.com/a-new-algorithm-for-finding-a-visual-center-of-a-polygon-7c77e6492fbc
All credit of the algorithm to them. I'm just a code monkey typing in numbers and hoping those numbers work.

Also there already is a port of polylabel in python here: github.com/Twista/python-polylabel
It works great! I just wanted to try and implement it myself
"""
import numpy as np
from visual_center.polygon import Polygon
import cv2
from typing import TypeVar

TQuadtree = TypeVar("TQuadtree", bound="Quadtree")

class Quadtree:
    ne: TQuadtree|None = None
    nw: TQuadtree|None = None
    se: TQuadtree|None = None
    sw: TQuadtree|None = None
    divided: bool = False
    
    def __init__(self, polygon: Polygon, x:int, y:int, size:int, precision:int=1) -> None:
        """
        Assign parameters to the quadtree. Also calculates the radius
        
        Args:
            x (int): The x coordinate of the center.
            y (int): The y coordinate of the center.
            size (int): The size of the quadtree. The quadtree is a square.
        """
        self.polygon = polygon
        self.x = x
        self.y = y
        self.size = size
        self.precision = precision
        
        # Radius is from the center to the corner
        self.radius = np.sqrt((size / 2)**2 + (size/2)**2)
        
        # Distance to the nearest polygon edge
        self.distance = polygon.signed_distance(np.array([x, y]))
        
        # Any point inside the cell can’t have a bigger distance to the polygon than this value
        self.cell_max = self.distance + self.radius
        
    def subdivide(self) -> list[TQuadtree]:
        """ Subdivide the quadtree into 4 smaller quadtree's. 
        
        Returns:
            A list of the new quadtree's. [NE, NW, SE, SW]
        """
        # Calculate the new width and height
        size = self.size
        
        # Create the new quadtree's
        self.ne = Quadtree(self.polygon, self.x + size/4, self.y - size/4, size/2, self.precision)
        self.nw = Quadtree(self.polygon, self.x - size/4, self.y - size/4, size/2, self.precision)
        self.se = Quadtree(self.polygon, self.x + size/4, self.y + size/4, size/2, self.precision)
        self.sw = Quadtree(self.polygon, self.x - size/4, self.y + size/4, size/2, self.precision)
        
        # Mark as divided
        self.divided = True
        
        # Return the new quadtree's
        return [self.ne, self.nw, self.se, self.sw]
    
    def draw(self, image:np.ndarray, color:tuple = (232, 122, 28, 255)) -> np.ndarray:
        """ Recursively draws the quadtree on the image
        
        Args:
            image (np.ndarray): The image to draw on.
            color (tuple): The color to draw the quadtree in.

        Returns:
            (np.ndarray) The image with the quadtree drawn on it.
        """
        # Draw box
        image = cv2.rectangle(image, 
            np.array((self.x - self.size//2, self.y - self.size//2), dtype=int), 
            np.array((self.x + self.size//2, self.y + self.size//2), dtype=int), 
            color, 1)
        
        # Draw center
        image = cv2.circle(image, np.array((self.x, self.y), dtype=int), 1, color, -1)  
          
        # If subdivided, draw the subdivisions
        if self.divided:
            image = self.ne.draw(image)
            image = self.nw.draw(image)
            image = self.se.draw(image)
            image = self.sw.draw(image)
        
        return image
    
def find_pole(shell:np.ndarray, holes:np.ndarray=[], precision: int=1, return_quadtree:bool=False) -> np.array:
    """
    Approximate the pole of inaccessability of the polygon.
    
    Args:
        shell (np.ndarray): The shell of the polygon.
        holes (np.ndarray): The holes in the polygon.
        precision (int): The precision of the quadtree. The lower the precision, the more accurate the result.
        return_quadtree (bool): If true, the quadtree will be returned as well.
    
    Returns:
        (np.ndarray) The pole of inaccessability of the polygon.
        (float) The distance to the pole of inaccessability.
        (Quadtree)[optional] The quadtree used to find the pole of inaccessability.
    """
    # Create polygon
    polygon:Polygon = Polygon(shell, holes)
    
    # Create the quadtree
    size:int = max(polygon.width, polygon.height) # Size of the first quad in the tree
     
    # Create the first quadtree to cover the polygon
    root:Quadtree = Quadtree(polygon, polygon.centroid[0], polygon.centroid[1], size, precision)
    
    # The largest quadtree distance to the polygon so far
    best_quad:Quadtree = root
    
    # Queue is used to store the quadtree's that need to be checked
    queue:list = [root]
    
    while len(queue):
        # Get the first quadtree in the queue
        qt:Quadtree = queue.pop(0)
        
        # Discard cell if distance from cell center to polygon plus cell radius is 
        # less than or equal to the best distance of a processed cell within a given precision
        if qt.cell_max <= best_quad.distance + precision:
            # Discard this quad cell
            continue
        
        # Check if the quadtree is the largest
        if qt.distance > best_quad.distance:
            best_quad = qt
        
        if qt.divided:
            # Quadtree should never be divided here
            raise Exception("Quadtree has already been divided when it shouldn't be.")
        
        # Subdivide the quadtree
        queue.extend(qt.subdivide())
    
    if return_quadtree:
        return np.array([best_quad.x, best_quad.y]), best_quad.distance, root
    return np.array([best_quad.x, best_quad.y]), best_quad.distance


def find_pole_polygon(polygon: Polygon, precision: int=1) -> np.array:
    """
    Approximate the pole of inaccessability of the polygon.
    
    Args:
        polygon (Polygon): The polygon.
        precision (int): The precision of the quadtree. The lower the precision, the more accurate the result.
    """
    return find_pole(polygon.shell, polygon.holes, precision)