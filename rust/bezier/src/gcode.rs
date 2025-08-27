use std::ops::{AddAssign};

struct OptPos {
    x: Option<f32>,
    y: Option<f32>,
    z: Option<f32>,
}

impl AddAssign for OptPos {
    fn add_assign(&mut self, other: OptPos) {
        if let Some(x) = other.x {
            self.x = Some(self.x.unwrap_or(0.0) + x);
        }
        if let Some(y) = other.y {
            self.y = Some(self.y.unwrap_or(0.0) + y);
        }
        if let Some(z) = other.z {
            self.z = Some(self.z.unwrap_or(0.0) + z);
        }
    }
}

pub struct GProg {
    commands : Vec<String>,
    pos : OptPos,
    relative : bool
}

impl GProg {
    pub fn new() -> Self {
        GProg { commands: Vec::new(), pos: OptPos { x: None, y: None, z: None }, relative: false }
    }

    pub fn units(&mut self, u: &str) -> &mut Self {
        match u {
            "mm" => {
                self.commands.push(format!("G21 ; set units to mm"));
            },
            "inch" => {
                self.commands.push(format!("G21 ; set units to inch"));
            },
            _ => {
                eprintln!("Unknown units: {}", u);
            }
        }
        self
    }
    pub fn coords(&mut self, c: &str) -> &mut Self {
        match c {
            "abs" => {
                self.commands.push(format!("G90 ; set coordinates to absolute"));
            },
            "rel" => {
                self.commands.push(format!("G91 ; set coordinates to relative"));
                self.relative = true;
            },
            _ => {
                eprintln!("Unknown coordinates mode: {}", c);
            }
        }
        self
    }
    pub fn feed_rate(&mut self, feed: f32) -> &mut Self {
        self.commands.push(format!("F{} ; set feed rate", feed));
        self
    }
    pub fn end(&mut self) -> &mut Self {
        self.commands.push("M30 ; end program".to_string());
        self
    }
    pub fn spindle_on(&mut self, speed_: Option<f32>) -> &mut Self {
        self.commands.push(
            match speed_ {
                Some(speed) => format!("M03 S{} ; spindle on", speed),
                None => "M03 ; spindle on".to_string(),
            }
        );
        self
    }
    pub fn spindle_off(&mut self) -> &mut Self {
        self.commands.push("M05 ; spindle off".to_string());
        self
    }
    fn move_coords(&mut self, to : OptPos) -> String {
        if to.x.is_some() || to.y.is_some() || to.z.is_some() {
            let mut cmd = String::new();
            if let Some(x) = to.x {
                cmd.push_str(&format!(" X{:.3}", x));
            }
            if let Some(y) = to.y {
                cmd.push_str(&format!(" Y{:.3}", y));
            }
            if let Some(z) = to.z {
                cmd.push_str(&format!(" Z{:.3}", z));
            }
            if self.relative {
                self.pos += to;
            } else {
                self.pos = to;
            }
            cmd
        } else {
            "G0".to_string()
        }
    }
    pub fn move_to(&mut self, to: OptPos) -> &mut Self {
        let coords = self.move_coords(to);
        self.commands.push(format!("G00{}", coords));
        self
    }
    pub fn x_move_to(&mut self, to: f32) -> &mut Self {
        self.move_to(OptPos { x: Some(to), y: None, z: None });
        self
    }
    pub fn y_move_to(&mut self, to: f32) -> &mut Self {
        self.move_to(OptPos { x: None, y: Some(to), z: None });
        self
    }
    pub fn z_move_to(&mut self, to: f32) -> &mut Self {
        self.move_to(OptPos { x: None, y: None, z: Some(to) });
        self
    }
    pub fn linear_to(&mut self, to: OptPos) -> &mut Self {
        let coords = self.move_coords(to);
        self.commands.push(format!("G01{}", coords));
        self
    }
    pub fn commend(&mut self, to :&str) -> &mut Self {
        self.commands.push(to.to_string());
        self
    }
    pub fn to_string(&self) -> String {
        self.commands.join("\n")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gprog() {
        let mut gprog = GProg::new();
        gprog.units("mm").coords("abs");
        assert_eq!(gprog.to_string(), "G21 ; set units to mm\nG90 ; set coordinates to absolute");
    }
}