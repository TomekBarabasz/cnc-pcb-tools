import re
from .common import Point2d
from .bezier import Bezier

def read_svg_paths(filename):
    import xml.etree.ElementTree as ET
    Paths = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    # Handle possible namespace
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"
    
    for path in root.findall(f".//{ns}path"):
        pid = path.get("id")
        d_attr = path.get("d")
        if not d_attr:
            continue  # skip paths without data
        
        Paths[pid] = d_attr
    
    return Paths

def parse_svg_path(path_str : str):
    """
    Parse an SVG path string and extract cubic Bezier curves.

    Args:
        path_str: SVG path data (the 'd' attribute of a <path>).

    Returns:
        A list of dicts, each representing a cubic Bezier segment with keys:
        - 'start': (x, y) start point
        - 'ctrl1': (x, y) first control point
        - 'ctrl2': (x, y) second control point
        - 'end': (x, y) end point
    """
    # Tokenize commands and numbers
    tokens = re.findall(r"[MmCcZz]|-?\d*\.?\d+(?:\.\d+)?", path_str)
    idx = 0
    current_pos = (0.0, 0.0)
    start_pos = (0.0, 0.0)
    current_cmd = None
    beziers = []

    while idx < len(tokens):
        token = tokens[idx]
        if token in "MmCcZz":
            current_cmd = token
            idx += 1
            if current_cmd in "Zz":
                current_pos = start_pos
            continue

        if current_cmd in ("M", "m"):
            x = float(tokens[idx])
            y = float(tokens[idx + 1])
            if current_cmd == "m":
                x += current_pos[0]
                y += current_pos[1]
            current_pos = (x, y)
            start_pos = (x, y)
            idx += 2

        elif current_cmd in ("C", "c"):
            is_relative = (current_cmd == "c")
            # consume groups of 6 numbers
            while idx + 5 < len(tokens) and re.match(r"-?\d", tokens[idx]):
                nums = list(map(float, tokens[idx:idx + 6]))
                if is_relative:
                    nums = [
                        nums[0] + current_pos[0], nums[1] + current_pos[1],
                        nums[2] + current_pos[0], nums[3] + current_pos[1],
                        nums[4] + current_pos[0], nums[5] + current_pos[1],
                    ]
                ctrl1 = (nums[0], nums[1])
                ctrl2 = (nums[2], nums[3])
                end   = (nums[4], nums[5])

                beziers.append(Bezier(start=Point2d.fromTuple(current_pos), 
                                      ctrl1=Point2d.fromTuple(ctrl1), 
                                      ctrl2=Point2d.fromTuple(ctrl2), 
                                      end=Point2d.fromTuple(end)))
                current_pos = end
                idx += 6

        else:
            idx += 1

    return beziers