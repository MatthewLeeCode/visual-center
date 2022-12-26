""" Functions for working with polygons."""
import cv2
import numpy as np


class Polygon:
    
    def __init__(self, shell: np.ndarray, holes:list[np.ndarray]=[]):
        """ Creates a polygon.
        
        Args:
            shell (np.ndarray): The shell of the polygon. Expects a numpy array of shape (n, 2).
                If the shape is (n, 1, 2), it will be reshaped to (n, 2). This is useful for cv2.findContours.
            holes (list[np.ndarray]): The holes in the polygon.
        """
        # Reshape the shell if needed
        if len(shell.shape) == 3:
            shell = shell.reshape(shell.shape[0], 2)
        
        # Reshape the holes if needed
        if len(holes) > 0:
            for i, hole in enumerate(holes):
                if len(hole.shape) == 3:
                    holes[i] = hole.reshape(hole.shape[0], 2)
        
        self.shell = shell
        self.holes = holes
        self._calculate_key_points()
    
    def _calculate_key_points(self):
        """ Calculates the key points of the polygon.
        
        Points:
            centroid (np.ndarray): The centroid of the polygon.
            width (int): The width of the polygon.
            height (int): The height of the polygon.
        """
        bbox = self._get_bbox()
        self.centroid = np.array([bbox[0], bbox[1]], dtype=int)
        self.width = bbox[2]
        self.height = bbox[3]
    
    def _get_bbox(self) -> list[np.ndarray]:
        """ Gets the key points of a polygon.
        
        Key points: x, y (centroid), width, height
        
        Args:
            polygon (np.ndarray): The polygon to get the key points from.
                Holes are not required as they are not used in the calculation
        
        Returns:
            A list of key points. [x(int), y(int), width(int), height(int)]
        """
        
        min_x = self.shell[:, 0].min()
        max_x = self.shell[:, 0].max()
        min_y = self.shell[:, 1].min()
        max_y = self.shell[:, 1].max()
        width = max_x - min_x
        height = max_y - min_y
        x = min_x + width // 2
        y = min_y + height // 2
        centroid = np.array([x, y], dtype=int)
        # Return the key points
        return [*centroid, width, height] # Width and height are always 1 more for some reason

    def signed_distance(self, point: np.ndarray) -> float:
        """ Calculates the distance from a point to the polygon edge.
        
        Works for any polygon, including with holes.
        
        Args:
            point (np.ndarray): The point to calculate the distance to.
            shell (np.ndarray): The shell of the polygon. Expects a numpy array of shape (n, 2).
                If the shape is (n, 1, 2), it will be reshaped to (n, 2). This is useful for cv2.findContours.
            holes (list[np.ndarray]): The holes in the polygon.

            
        Returns:
            The minimum distance to the polygon edge. Positive if the point is inside the polygon, negative if outside.
        """
        # Ensure point is of type 
        point = np.array(point, dtype=np.float32)
        
        # Calculate the distance to the shell
        min_dist = cv2.pointPolygonTest(self.shell, point, True)  

        for hole in self.holes:
            # We need to invert the distance, since we dont want the point inside the hole
            hole_dist = cv2.pointPolygonTest(hole, point, True) * -1
            # Get the minimum distance
            if abs(hole_dist) < abs(min_dist):
                min_dist = hole_dist
            
        return min_dist
