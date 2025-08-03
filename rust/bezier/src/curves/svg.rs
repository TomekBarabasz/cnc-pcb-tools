use std::collections::HashMap;
use std::error::Error;
use std::fs;

pub fn read_svg_paths(filename: &str) -> Result<HashMap<String, String>, Box<dyn Error>> {
    let contents = fs::read_to_string(filename)?;
    let doc = roxmltree::Document::parse(&contents)?;
    let root = doc.root_element();

    let mut paths = HashMap::new();
    collect_paths_recursive(root, &mut paths);

    Ok(paths)
}

fn collect_paths_recursive<'a>(node: roxmltree::Node<'a, 'a>, paths: &mut HashMap<String, String>) {
    for child in node.children() {
        if child.is_element() {
            let tag_name = child.tag_name().name(); // Ignores namespace
            match tag_name {
                "path" => {
                    if let (Some(id), Some(d)) = (child.attribute("id"), child.attribute("d")) {
                        paths.insert(id.to_string(), d.to_string());
                    }
                }
                _ => {
                    // Recurse into any other container, e.g., <g>, <svg>, etc.
                    collect_paths_recursive(child, paths);
                }
            }
        }
    }
}