import math

def point_line_distance(pt, line_start, line_end):
    x0, y0 = pt
    x1, y1 = line_start
    x2, y2 = line_end
    num = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2*y1 - y2*x1)
    den = math.hypot(x2 - x1, y2 - y1)
    return num / den if den != 0 else 0

def midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def normalize(v):
    length = math.hypot(v[0], v[1])
    return (v[0]/length, v[1]/length) if length != 0 else (0, 0)

def perpendicular(v):
    return (-v[1], v[0])

class Point2d:
    @staticmethod
    def fromTuple(t):
        return Point2d(t[0],t[1])
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Point2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point2d(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Point2d(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        return Point2d(self.x / scalar, self.y / scalar)
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def distance_to_line(self, line_start, line_end):
        x0, y0 = self.x,self.y
        x1, y1 = line_start.x, line_start.y
        x2, y2 = line_end.x, line_end.y
        num = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2*y1 - y2*x1)
        den = math.hypot(x2 - x1, y2 - y1)
        return num / den if den != 0 else 0
    
    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2)
        if length == 0:
            return Point2d(0, 0)
        return Point2d(self.x / length, self.y / length)
    
    def perpendicular(self):
        """Return perpendicular vector (rotated 90 degrees counter-clockwise)"""
        return Point2d(-self.y, self.x)
    
    def midpoint(self, other):
        return (self + other) / 2
    
    def toTuple(self):
        return (self.x, self.y)
    
    def __repr__(self):
        return f"Point2d({self.x:.3f}, {self.y:.3f})"