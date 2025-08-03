use crate::curves::point::Point;

#[derive(Debug, Clone, Copy)]
pub struct Bezier {
    pub start : Point,
    pub c1    : Point,
    pub c2    : Point,
    pub end   : Point,
}

impl Bezier {
    pub fn new(start: Point, c1: Point, c2: Point, end: Point) -> Self {
        Bezier { start, c1, c2, end }
    }

    pub fn point_at(&self, t: f32) -> Point {
        let u = 1.0 - t;
        let tt = t * t;
        let uu = u * u;
        let uuu = uu * u;
        let ttt = tt * t;

        let p = self.start * uuu; // (1-t)^3 * P0
        let p1 = self.c1 * (3.0 * uu * t); // 3(1-t)^2 * t * P1
        let p2 = self.c2 * (3.0 * u * tt); // 3(1-t) * t^2 * P2
        let p3 = self.end * ttt; // t^3 * P3

        p + p1 + p2 + p3
    }

    pub fn subdivide(&self) -> (Bezier, Bezier) {
        let mid1 = Point::midpoint(&self.start, &self.c1);
        let mid2 = Point::midpoint(&self.c1, &self.c2);
        let mid3 = Point::midpoint(&self.c2, &self.end);
        let mid12 = Point::midpoint(&mid1, &mid2);
        let mid23 = Point::midpoint(&mid2, &mid3);

        (
            Bezier {
                start: self.start,
                c1: mid1,
                c2: mid12,
                end: mid23,
            },
            Bezier {
                start: mid23,
                c1: mid12,
                c2: mid3,
                end: self.end,
            },
        )
    }

    fn flatten(&self, tolerance: f32) -> Vec<Point> {
        let d1 = self.c1.distance_to_line(&self.start, &self.end);
        let d2 = self.c2.distance_to_line(&self.start, &self.end);
        if f32::max(d1, d2) < tolerance {
            return vec![self.start, self.end];
        } else {
            let (left, right) = self.subdivide();
            let mut points = left.flatten(tolerance);
            points.pop(); // Remove the last point to avoid duplicates
            points.extend(right.flatten(tolerance));
            points
        }
    }
}
