""" 
Finding the visual center / pole of inaccessability / largest inscribed circle / point that is furthest from the edge of a polygon 
using a quadtree. 

Implementation completely based off of the mapbox implementation: https://blog.mapbox.com/a-new-algorithm-for-finding-a-visual-center-of-a-polygon-7c77e6492fbc
All credit of the algorithm to them. I'm just a code monkey typing in numbers and hoping those numbers work.
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
    
    def __init__(self, polygon: Polygon, x:int, y:int, width:int, height:int, precision:int=1) -> None:
        """
        Assign parameters to the quadtree. Also calculates the radius
        
        Args:
            x (int): The x coordinate of the center.
            y (int): The y coordinate of the center.
            width (int): The width of the quadtree.
            height (int): The height of the quadtree.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.precision = precision
        
        # Radius is from the center to the corner
        self.radius = np.sqrt((width / 2)**2 + (height/2)**2)
        
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
        new_width = self.width / 2
        new_height = self.height / 2
        
        # Create the new quadtree's
        self.ne = Quadtree(self.polygon, self.x + new_width, self.y - new_height, new_width, new_height, self.precision)
        self.nw = Quadtree(self.polygon, self.x - new_width, self.y - new_height, new_width, new_height, self.precision)
        self.se = Quadtree(self.polygon, self.x + new_width, self.y + new_height, new_width, new_height, self.precision)
        self.sw = Quadtree(self.polygon, self.x - new_width, self.y + new_height, new_width, new_height, self.precision)
        
        # Mark as divided
        self.divided = True
        
        # Return the new quadtree's
        return [self.ne, self.nw, self.se, self.sw]