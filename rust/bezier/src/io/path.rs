use crate::bezier::Bezier;
use crate::point::Point;
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
    I: Iterator<Item = &'a str>,
{
    let chunk = chunk_iter.next().ok_or(ParseError::InvalidPath)?;
    let mut p = Point::from_str(chunk).ok_or(ParseError::InvalidPoint)?;
    if relative {
        p += *st;
    }
    Ok(p)
}

fn curve_to<'a,I>(st: &Point, relative: bool, chunk_iter: &mut Peekable<I>) -> Result<Bezier, ParseError>
where
    I: Iterator<Item = &'a str>,
{
    let chunk = chunk_iter.next().ok_or(ParseError::InvalidPath)?;
    let mut c1  = Point::from_str(chunk).ok_or(ParseError::InvalidPoint)?;
    let chunk = chunk_iter.next().ok_or(ParseError::InvalidPath)?;
    let mut c2  = Point::from_str(chunk).ok_or(ParseError::InvalidPoint)?;
    let chunk = chunk_iter.next().ok_or(ParseError::InvalidPath)?;
    let mut end = Point::from_str(chunk).ok_or(ParseError::InvalidPoint)?;
    if relative {
        c1 += *st;
        c2 += *st;
        end += *st;
    }
    Ok(Bezier::new(*st, c1, c2, end))
}

fn line_to<'a,I>(st: &Point, relative: bool, chunk_iter: &mut Peekable<I>) -> Result<Bezier, ParseError>
where
    I: Iterator<Item = &'a str>,
{
    let chunk = chunk_iter.next().ok_or(ParseError::InvalidPath)?;
    let d;
    let end;
    if relative {
        d = Point::from_str(chunk).ok_or(ParseError::InvalidPoint)?;
        end = st + &d;  //Add for &Point
    }
    else {
        end = Point::from_str(chunk).ok_or(ParseError::InvalidPoint)?;
        d = end - *st;  //Add for Point
    }
    let c1 = (*st + d) / 3.0;
    let c2 = (*st + d * 2.0) / 3.0;
    Ok(Bezier::new(*st, c1, c2, end))
}

pub fn parse_svg_path(path : &str) -> Result<Vec<Bezier>, ParseError> {
    let mut bezier_curves = Vec::new();
    let mut current_point = Point::new(0.0, 0.0);
    let mut chunk_iter = path.split_whitespace().peekable();
    let mut cmd = Command::ClosePath;
    let mut relative = false;
    while let Some(chunk) = chunk_iter.peek() {
        // check first character of a chunk to determine command
        let c = chunk.chars().next().unwrap();

        if c.is_alphabetic() {
            relative = c.is_lowercase();
            // Command character
            cmd = match c {
                'M' | 'm' => Command::MoveTo,
                'C' | 'c' => Command::CurveTo,
                'Z' | 'z' => Command::ClosePath,
                'L' | 'l' => Command::LineTo,
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
            Command::LineTo => {
                let bezier = line_to(&current_point, relative, &mut chunk_iter)?;
                bezier_curves.push(bezier);
                current_point = bezier.end;
                println!("{} from {} to {}", if relative {'l'} else {'L'}, bezier.start, bezier.end);
            }
        }
    }
    Ok(bezier_curves)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_svg_path() {
        let path = "M 10,10 C 20,20 30,30 40,40";
        let curves = parse_svg_path(path).unwrap();
        assert_eq!(curves.len(), 1);
    }

    #[test]
    fn test_parse_svg_path_with_multiple_curves() {
        let path = "M 1,1 C 2,2 3,3 4,4 c 5,5 6,6 7,7 m 8,8 C 9,9 10,10 11,11";
        let curves = parse_svg_path(path).unwrap();
        assert_eq!(curves.len(), 3);
    }

    #[test]
    fn test_parse_invalid_path_incomplete_curve() {
        let path = "M 1,1 C 2,2 3,3";
        let result = parse_svg_path(path);
        assert!(matches!(result, Err(ParseError::InvalidPath)));
    }

    #[test]
    fn test_parse_invalid_path_incomplete_move() {
        let path = "M";
        let result = parse_svg_path(path);
        assert!(matches!(result, Err(ParseError::InvalidPath)));
    }

    #[test]
    fn test_parse_invalid_path_missing_curve_control_point() {
        let path = "M 1,1 C 2,2";
        let result = parse_svg_path(path);
        assert!(matches!(result, Err(ParseError::InvalidPath)));
    }

    #[test]
    fn test_parse_invalid_path_invalid_command() {
        let path = "M 1,1 d 2,2 3,3 4,4";
        let result = parse_svg_path(path);
        assert!(matches!(result, Err(ParseError::InvalidCommand)));
    }

    #[test]
    fn test_parse_invalid_path_invalid_point() {
        let path = "M 1,1 C 2 3,3 4,4";
        let result = parse_svg_path(path);
        assert!(matches!(result, Err(ParseError::InvalidPoint)));
    }

    #[test]
    fn test_parse_invalid_path_invalid_coord() {
        let path = "M 1,1 C ?,3,3 4,4";
        let result = parse_svg_path(path);
        assert!(matches!(result, Err(ParseError::InvalidPoint)));
    }   

    #[test]
    fn test_line_to_bezier_conversion() {
        let path = "M 0,0 L 30,30";
        let result = parse_svg_path(path).unwrap();
        
        assert_eq!(result.len(), 1);
        let bezier = &result[0];
        assert_eq!(bezier.start, Point::new(0.0, 0.0));
        assert_eq!(bezier.end, Point::new(30.0, 30.0));
        // Control points should be on the line
        assert_eq!(bezier.c1, Point::new(10.0, 10.0));
        assert_eq!(bezier.c2, Point::new(20.0, 20.0));
    }
}