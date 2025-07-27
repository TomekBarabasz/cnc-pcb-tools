from .common import *
from dataclasses import dataclass

@dataclass
class Line:
    start : Point2d
    end   : Point2d
    def toTuple(self):
        return (self.start, self.end)
    @staticmethod
    def fromTuple(start,end):
        return Line(start,end)
    def toXY(self):
        return zip(*self.toTuple())

@dataclass
class Bezier:
    start : Point2d
    ctrl1 : Point2d
    ctrl2 : Point2d
    end   : Point2d

    def subdivide(self):
        p01 = self.start.midpoint(self.ctrl1)
        p12 = self.ctrl1.midpoint(self.ctrl2)
        p23 = self.ctrl2.midpoint(self.end)
        p012 = p01.midpoint(p12)
        p123 = p12.midpoint(p23)
        p0123 = p012.midpoint(p123)
        return Bezier(self.start, p01, p012, p0123),Bezier(p0123,p123,p23,self.end)

    def flatten(self, max_error):
        d1 = self.ctrl1.distance_to_line(self.start, self.end)
        d2 = self.ctrl2.distance_to_line(self.start, self.end)
        if max(d1, d2) <= max_error:
            return (self.start,self.end)
        else:
            left,right = self.subdivide()
            return left.flatten(max_error)[:-1] + right.flatten(max_error)

def subdivide_bezier(p0, p1, p2, p3):
    p01 = midpoint(p0, p1)
    p12 = midpoint(p1, p2)
    p23 = midpoint(p2, p3)
    p012 = midpoint(p01, p12)
    p123 = midpoint(p12, p23)
    p0123 = midpoint(p012, p123)
    return (p0, p01, p012, p0123), (p0123, p123, p23, p3)

def flatten_bezier(p0, p1, p2, p3, max_error):
    d1 = point_line_distance(p1, p0, p3)
    d2 = point_line_distance(p2, p0, p3)
    if max(d1, d2) <= max_error:
        return [p0, p3]
    else:
        left, right = subdivide_bezier(p0, p1, p2, p3)
        return flatten_bezier(*left, max_error)[:-1] + flatten_bezier(*right, max_error)
