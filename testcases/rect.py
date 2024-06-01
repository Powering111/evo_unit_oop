# Rectangle implementation for development
# Simple control flow

from typing_extensions import Self

class InvalidArgumentException(Exception):
    pass

class Point:
    def __init__(self, x:float, y:float):
        self.x=x
        self.y=y
    
    def __str__(self) -> str:
        return f"({self.x},{self.y})"

# Rectangle in R^2.
class Rectangle:
    # x,y is the cartesian coordinate of bottom left corner of this rectangle.
    def __init__(self, x:float, y:float, width:float, height:float):
        if width<=0 or height<=0:
            pass
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2*(self.width+self.height)

    def is_square(self) -> bool:
        if self.width == self.height:
            return True
        else:
            return False

    def contains(self, point: Point) -> bool:
        return (self.x<=point.x and point.x<=self.x+self.width) and (self.y<=point.y and point.y <= self.y+self.height)

    def contains_origin(self) -> bool:
        return self.contains(Point(0,0))

    def center_of_mass(self) -> Point:
        return Point(self.x+self.width/2, self.y+self.height/2)
    
    def __eq__(self, other: Self) -> bool:
        return (self.x==other.x and self.y==other.y and self.width==other.width and self.height==other.height)

    def __str__(self) -> str:
        return f"Rect({self.x},{self.y},{self.width},{self.height})"
