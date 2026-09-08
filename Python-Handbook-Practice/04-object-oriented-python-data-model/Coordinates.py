"""
Immutable Coordinate / Cache Key
building a cache where coordinates are used as dictionary keys.
"""

class Coordinates:
    x: int 
    y: int 
    def __init__(self, x, y):
        self.x = x 
        self.y = y 


loc1 = Coordinates(-0.23, 50.4)
loc2 = Coordinates(-0.27, 70.4)

loc_dict = {}
loc_dict[loc1] = "Location 1"
loc_dict[loc2] = "Location 2"

print(repr(loc_dict))