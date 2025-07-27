
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Point {
    pub x: f32,
    pub y: f32
}

use std::ops::{Add,AddAssign,Sub,Mul,Div};
use std::fmt;

impl Add for &Point {
    type Output = Point;
    fn add(self, other: &Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}
// Point + Point hould work via deref coercion without Add for Point
// dont know why it is not
impl Add for Point {
    type Output = Point;
    fn add(self, other: Point) -> Point {
        // Delegate to the reference implementation
        &self + &other
    }
}

impl AddAssign for Point {
    fn add_assign(&mut self, other: Point) {
        self.x += other.x;
        self.y += other.y;
    }
}

impl Sub for &Point {
    type Output = Point;
    fn sub(self, other: &Point) -> Point {
        Point {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}
impl Sub for Point {
    type Output = Point;
    fn sub(self, other: Point) -> Point {
        // Delegate to the reference implementation
        &self - &other
    }
}
impl Mul<f32> for &Point {
    type Output = Point;
    fn mul(self, scalar: f32) -> Point {
        Point {
            x: self.x * scalar,
            y: self.y * scalar,
        }
    }
}
impl Mul<f32> for Point {
    type Output = Point;
    fn mul(self, scalar: f32) -> Point {
        &self * scalar
    }
}
impl Div<f32> for &Point {
    type Output = Point;
    fn div(self, divisor: f32) -> Point {
        if divisor == 0.0 {
            panic!("Division by zero is not allowed");
        }
        Point {
            x: self.x / divisor,
            y: self.y / divisor,
        }
    }
}
impl Div<f32> for Point {
    type Output = Point;
    fn div(self, divisor: f32) -> Point {
        &self / divisor
    }
}
impl Point {
    pub fn new(x: f32, y: f32) -> Self {
        Point { x, y }
    }
    pub fn dot(&self, other: &Point) -> f32 {
        self.x * other.x + self.y * other.y
    }
    pub fn distance(&self, other: &Point) -> f32 {
        let d = self - other;
        d.dot(&d).sqrt()
    }
    pub fn distance_to_line(&self, a: &Point, b: &Point) -> f32 {
        let ab = b - a;
        let ap = self - a;
        let area = ab.x * ap.y - ab.y * ap.x; // Cross product
        let base = ab.distance(a);
        area.abs() / base
    }
    pub fn midpoint(a: &Point, b: &Point) -> Point {
        (a + b) / 2.0
    }
    pub fn interpolate(&self, other: &Point, t: f32) -> Point {
        *self + (other - self) * t
    }
    pub fn from_str(s: &str) -> Option<Point> {
        if let Some((x_str, y_str)) = s.split_once(',') {
            if let (Ok(x), Ok(y)) = (x_str.trim().parse::<f32>(), y_str.trim().parse::<f32>()) {
                return Some(Point::new(x, y));
            }
        }
        None
    }
}
impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{},{}", self.x, self.y)
    }
}