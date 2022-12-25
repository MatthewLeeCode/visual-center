""" 
Approximating (Really close approximation) of the visual center / pole of inaccessability / largest inscribed circle / point that is furthest from the edge of a polygon 
using a quadtree. 

Implementation completely based off of the polylabel implementation: blog.mapbox.com/a-new-algorithm-for-finding-a-visual-center-of-a-polygon-7c77e6492fbc
All credit of the algorithm to them. I'm just a code monkey typing in numbers and hoping those numbers work.

Also there already is a port of polylabel in python here: github.com/Twista/python-polylabel
It works great! I just wanted to try and implement it myself. Also unsure how well it works with polygons with holes (Didn't try. It might. I don't know.)
"""
import numpy as np
from polygon import Polygon
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
        size = self.size / 2
        
        # Create the new quadtree's
        self.ne = Quadtree(self.polygon, self.x + size, self.y - size, size, self.precision)
        self.nw = Quadtree(self.polygon, self.x - size, self.y - size, size, self.precision)
        self.se = Quadtree(self.polygon, self.x + size, self.y + size, size, self.precision)
        self.sw = Quadtree(self.polygon, self.x - size, self.y + size, size, self.precision)
        
        # Mark as divided
        self.divided = True
        
        # Return the new quadtree's
        return [self.ne, self.nw, self.se, self.sw]
    
    
def find_pole(shell:np.ndarray, holes:np.ndarray=[], precision: int=1) -> np.array:
    """
    Approximate the pole of inaccessability of the polygon.
    
    Args:
        shell (np.ndarray): The shell of the polygon.
        holes (np.ndarray): The holes in the polygon.
        precision (int): The precision of the quadtree. The lower the precision, the more accurate the result.
    """
    # Create polygon
    polygon:Polygon = Polygon(shell, holes)
    
    # Create the quadtree
    size:int = max(polygon.width, polygon.height) # Size of the first quad in the tree
    
    # Create the first quadtree to cover the polygon
    qt:Quadtree = Quadtree(polygon, polygon.centroid[0], polygon.centroid[1], size, precision)
    
    # The largest quadtree distance to the polygon so far
    best_quad:Quadtree = qt
    
    # Queue is used to store the quadtree's that need to be checked
    queue:list = [qt]
    
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
    
    return np.array([best_quad.x, best_quad.y]), best_quad.distance


def find_pole_polygon(polygon: Polygon, precision: int=1) -> np.array:
    """
    Approximate the pole of inaccessability of the polygon.
    
    Args:
        polygon (Polygon): The polygon.
        precision (int): The precision of the quadtree. The lower the precision, the more accurate the result.
    """
    return find_pole(polygon.shell, polygon.holes, precision)