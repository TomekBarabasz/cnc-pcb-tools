use crate::bezier::Bezier;
use crate::point::Point;
use regex::Regex;
use std::iter::Peekable;

enum Command {
    MoveTo,
    CurveTo,
    LineTo,
    ClosePath,
}

#[derive(Debug)]
pub enum ParseError {
    InvalidCommand,
    InvalidPath,
    InvalidPoint,
}

fn move_to<'a,I>(st: &Point, relative: bool, chunk_iter: &mut Peekable<I>) -> Result<Point, ParseError>
where
    I: Iterator<Item = regex::Match<'a>>,  if regex.find_iter is used
{
    let chunk = chunk_iter.next().ok_or(ParseError::InvalidPath)?;
    let mut p = Point::from_str(chunk.as_str()).ok_or(ParseError::InvalidPoint)?;
    if relative {
        p += *st;
    }
    Ok(p)
}

fn curve_to<'a,I>(st: &Point, relative: bool, chunk_iter: &mut Peekable<I>) -> Result<Bezier, ParseError>
where
    I: Iterator<Item = regex::Match<'a>>,
{
    let chunk = chunk_iter.next().ok_or(ParseError::InvalidPath)?;
    let mut c1  = Point::from_str(chunk.as_str()).ok_or(ParseError::InvalidPoint)?;
    let chunk = chunk_iter.next().ok_or(ParseError::InvalidPath)?;
    let mut c2  = Point::from_str(chunk.as_str()).ok_or(ParseError::InvalidPoint)?;
    let chunk = chunk_iter.next().ok_or(ParseError::InvalidPath)?;
    let mut end = Point::from_str(chunk.as_str()).ok_or(ParseError::InvalidPoint)?;
    if relative {
        c1 += *st;
        c2 += *st;
        end += *st;
    }
    Ok(Bezier::new(*st, c1, c2, end))
}

pub fn parse_svg_path(path : &str) -> Result<Vec<Bezier>, ParseError> {
    let mut bezier_curves = Vec::new();
    let mut current_point = Point::new(0.0, 0.0);
    let re = Regex::new(r"[a-zA-Z]|-?\d*\.?\d+,-?\d*\.?\d+").unwrap();
    if false {
        // printing
        for m in re.find_iter(path) {
            println!("{}", m.as_str());
        }
    }
    let mut chunk_iter = re.find_iter(path).peekable();
    let mut cmd = Command::ClosePath;
    let mut relative = false;
    while let Some(m) = chunk_iter.peek() {
        // check first character of a chunk to determine command
        let c = m.as_str().chars().next().unwrap();
        
        if c.is_alphabetic() {
            relative = c.is_lowercase();
            // Command character
            cmd = match c {
                'M' | 'm' => Command::MoveTo,
                'C' | 'c' => Command::CurveTo,
                'Z' | 'z' => Command::ClosePath,
                _ => return Err(ParseError::InvalidCommand), // Unsupported command
            };
            chunk_iter.next(); // Consume the command character
        } else {
            // not a command character - repeat the last one
        }
        match cmd {
            Command::MoveTo => {
                current_point = move_to(&current_point, relative, &mut chunk_iter)?;
                println!("{} {}", if relative {'m'} else {'M'}, current_point);
            }
            Command::CurveTo => {
                let bezier = curve_to(&current_point, relative, &mut chunk_iter)?;
                bezier_curves.push(bezier);
                current_point = bezier.end;
                println!("{} from {} to {}", if relative {'c'} else {'C'}, bezier.start, bezier.end);
            }
            Command::ClosePath => {
                // Close path logic can be added here if needed
            }
        }    
    }
    Ok(bezier_curves)
}
