mod curves;
use curves::{Point,Bezier};
use curves::svg::read_svg_paths;
use curves::parse_svg_path;
use std::path::{Path,PathBuf};
use clap::{Parser,Subcommand};
use std::collections::HashMap;
mod gcode;
use gcode::{GProg,OptPos};
use std::fs;

// rust-logo: "C:\tomek\projects\rustlings\website\static\images\rust_logo.svg"
// c:\tomek\cnc\visiorek.svg

fn test1() {

    let p1 = Point {x:0.0, y:0.0};
    let p2 = Point::new(1.0, 1.0);

    let p3 = p1 + p2;
    dbg!(p3);

    let curves = parse_svg_path("M 18.305942,11.739082 C 19.377937,16.46014 15.440135,25.154584 10.185389,30.233537 4.184859,24.854689 1.0356561,17.18134 1.2145156,10.421087 1.3933752,3.6608348 5.4841605,1.1100861 10.142875,1.1100861 c 4.658715,0 6.504945,3.1763541 6.504945,6.4624299 0,3.286077 -1.975106,4.889339 -4.209084,4.889339 -2.233978,0 -3.4029644,-0.272006 -3.9965028,-2.33838 -0.2121747,-2.5175536 1.2329631,-3.1886987 1.2329631,-3.1886987 0,0 -0.010115,2.5934755 1.8281877,2.5509597 1.838322,-0.042516 1.913222,-1.4282141 1.913222,-2.5509597 0,-1.122746 -0.934122,-2.4234115 -3.868956,-2.4234115 -2.934833,0 -4.6767591,3.2675769 -4.6767591,5.6971422 0,2.429566 2.0802103,5.314498 5.3144971,5.314498 3.234288,0 5.935989,-0.924155 8.120554,-3.783923 z").unwrap();
}

#[derive(Parser)]
#[command(version, about, long_about = None)]
struct Args {
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand,Debug)]
enum Commands {
    ToGcode {
        #[arg(value_name="INPUT")]
        filename: PathBuf,

        #[arg(short, long, value_name="OUTPUT")]
        output: PathBuf,

        #[arg(short, long, default_value_t = 0.01)]
        error: f32,

        #[arg(short, long)]
        tool_dia: f32,
    },
    Cmd1 {
        filename: PathBuf,

        #[arg(short, long)]
        output: Option<PathBuf>,
    },
    Cmd2 {
        #[arg(short, long)]
        filename: PathBuf,

        #[arg(short, long)]
        output: Option<PathBuf>,
    },
}

impl OptPos {
    fn from_pt( pt : Point) -> Self {
        OptPos {x : Some(pt.x), y : Some(pt.y), z : None}
    }
}

fn toGcode(filename : &Path, output: &Path, tolerance: f32, tool_dia: f32) {
    let paths = read_svg_paths(filename).unwrap();
    let curves = paths.iter()
                    .filter_map(|(name, p)| match parse_svg_path(p) {
                        Ok(bezier) => Some((name.clone(), bezier)),
                        Err(_) => {
                            eprintln!("Failed to parse SVG path {}", name);
                            None
                        },
                    })
                    .collect::<HashMap<String, Vec<Bezier>>>();
    // dbg!(&curves);
    /*
    let mut pts  = vec![];
    for (_,path) in curves.into_iter() {
        for c in path.iter() {
            pts.append( &mut c.flatten(tolerance) )
        }
    } or */

    let mut gprog = GProg::new();
    gprog.units("mm").coords("abs");
    
    /*
    let pts = curves.into_iter()
        .flat_map(|(_,path)| {
            path.into_iter()
            .flat_map(|c| c.flatten(tolerance))
        })
        .collect::<Vec<Point>>();
    */
    for (name,path) in curves.into_iter() {
        gprog.comment(&name);
        let pts : Vec<_> = path.into_iter().flat_map(|c| c.flatten(tolerance)).collect();
        let mut it = pts.into_iter();
        let p = it.next().unwrap();
        gprog.move_to( OptPos::from_pt(p) );
        for p in it {
            gprog.linear_to( OptPos::from_pt(p) );
        }
    }

    let res = fs::write(output, gprog.to_string());
}

fn main() {
    let cli = Args::parse();

    match cli.command {
        Some(Commands::ToGcode { filename, output, error, tool_dia }) => {
            println!("Flattening file: {:?}", filename);
            println!("Output file: {:?}", output);
            println!("Error tolerance: {}", error);
            println!("Tool diameter: {}", tool_dia);
            toGcode(&filename, &output, error, tool_dia);
        },
        Some(Commands::Cmd1 { filename, output }) => {
            println!("Command 1 with file: {:?}", filename);
            println!("Output file: {:?}", output);
        },
        Some(Commands::Cmd2 { filename, output }) => {
            println!("Command 2 with file: {:?}", filename);
            println!("Output file: {:?}", output);
        },
        None => {
            eprintln!("No command provided.");
        }
    }
}
