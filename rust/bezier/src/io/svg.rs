use serde::Deserialize;
use std::collections::HashMap;
use std::fs;
use std::error::Error;

#[derive(Debug, Deserialize)]
struct Svg {
    #[serde(rename = "path", default)]
    paths: Vec<PathElement>,
}

#[derive(Debug, Deserialize)]
struct PathElement {
    #[serde(rename = "id", default)]
    id: Option<String>,

    #[serde(rename = "d", default)]
    d: Option<String>,
}

pub fn read_svg_paths(filename: &str) -> Result<HashMap<String, String>, Box<dyn Error>> {
    let xml_content = fs::read_to_string(filename)?;
    let svg: Svg = serde_xml_rs::from_str(&xml_content)?;

    let mut paths_map = HashMap::new();
    for path in svg.paths {
        if let (Some(id), Some(d)) = (path.id, path.d) {
            paths_map.insert(id, d);
        }
    }

    Ok(paths_map)
}