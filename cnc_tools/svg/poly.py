from .common import *
import math

def arc_points(center, radius, start_angle, end_angle, steps=5):
    """Return CCW arc points from start_angle to end_angle"""
    if end_angle < start_angle:
        end_angle -= 2 * math.pi
    return [
        (
            center[0] + radius * math.cos(a),
            center[1] + radius * math.sin(a)
        )
        for a in [start_angle + i * (end_angle - start_angle) / steps for i in range(steps + 1)]
    ]

def outset_polyline_with_round_joins(flat_pts, offset_distance, closed=False, **kwargs):
    offset_poly = []
    normals = []
    count = len(flat_pts)
    arc_steps = kwargs.get('arc_steps',6) 
    loop_range = range(count) if closed else range(count - 1)

    for i in loop_range:
        i1 = i
        i2 = (i + 1) % count
        p_start, p_end = flat_pts[i1], flat_pts[i2]
        dir_vec = p_end - p_start
        normal = dir_vec.perpenicular().normalize()
        normals.append( (p_start, normal) )
        offset_vec = normal * offset_distance
        off_start = (p_start[0] + offset_vec[0], p_start[1] + offset_vec[1])
        off_end = (p_end[0] + offset_vec[0], p_end[1] + offset_vec[1])

        if i == 0:
            offset_poly.append(off_start)
        else:
            # Add arc at join
            prev_dir = (flat_pts[i1][0] - flat_pts[i1 - 1][0], flat_pts[i1][1] - flat_pts[i1 - 1][1])
            prev_norm = normalize(perpendicular(prev_dir))
            curr_norm = normal
            avg_norm = normalize((prev_norm[0] + curr_norm[0], prev_norm[1] + curr_norm[1]))
            arc_center = (flat_pts[i1][0] + avg_norm[0] * offset_distance,
                          flat_pts[i1][1] + avg_norm[1] * offset_distance)
            a1 = math.atan2(prev_norm[1], prev_norm[0])
            a2 = math.atan2(curr_norm[1], curr_norm[0])
            arc = arc_points(arc_center, offset_distance, a1, a2, arc_steps)
            offset_poly.extend(arc[1:])

        offset_poly.append(off_end)

    return offset_poly, normals

def outset_polyline(flat_pts, offset_distance, closed=False, **kwargs):
    offset_poly = []
    normals = []
    count = len(flat_pts)
    loop_range = range(count) if closed else range(count - 1)

    for i in loop_range:
        i1 = i
        i2 = (i + 1) % count
        p_start, p_end = flat_pts[i1], flat_pts[i2]
        dir_vec = p_end - p_start
        normal = dir_vec.perpendicular().normalize()
        normals.append( (p_start, normal) )
        offset_vec = normal * offset_distance
        off_start = p_start + offset_vec
        off_end = p_end + offset_vec
        

        offset_poly.append(off_end)

    return offset_poly, normals

def poly_to_toolpath(poly, tool_radius=5.0, outward=True, closed=False, round_joins=False):
    """Return toolpath as list of (x, y) points"""
    sign = 1 if outward else -1
    foo = outset_polyline_with_round_joins if round_joins else outset_polyline
    return foo(poly, offset_distance=sign * tool_radius, closed=closed, arc_steps=6)