import cnc_tools
import argparse
from math import ceil

def parse_args():
    parser = argparse.ArgumentParser(description='Generate G-code for the top part with inner and outer rings and center hole.')
    parser.add_argument('output_file', type=str, help='Output G-code file')
    parser.add_argument('--tool_dia', type=float, default=1.5, help='Tool diameter in mm (default: 1.5mm)')
    parser.add_argument('--tool_overlap_mm', type=float, default=None, help='Tool overlap in mm (default: 2/3 of tool diameter)')
    parser.add_argument('--tool_overlap_pct', type=float, default=30, help='Tool overlap in percent (default: 2/3 of tool diameter)')
    return parser.parse_args()

Pt = cnc_tools.Point
args = parse_args()
tool_dia = args.tool_dia
tool_overlap = args.tool_overlap_mm if args.tool_overlap_mm is not None else (tool_dia * args.tool_overlap_pct / 100 )

p = cnc_tools.GProg()
p.tool_dia(tool_dia)
p.tool_overlap(mm=tool_overlap)
p.z_travel(0)

center = Pt(0,0)
p.move(to=center)
p.spindle_on()

# center hole : diameter 5mm depth 9mm
p.comment("Center hole")
p.feed_rate(200)
depth = list(range(-1,-10,-1))
p.cylinder(center, radius=2.5, depth=depth) #optional overwrite tool_overlap_mm)

tr = p.get_tool_radius()
outer_ring_start = 13.5
inner_ring_center = outer_ring_start - 7 + tr

p.comment("Inner ring")
p.circle(center, radius = inner_ring_center, depth=depth) #current tool diameter

# channel between inner and outer ring
p.comment("channel between inner and outer ring")
p.line(Pt(inner_ring_center,0), Pt(outer_ring_start,0), depth=depth, f=200, end_point='end')

p.comment("Outer ring")
width = 5.5
p.ring(center, radius_from = outer_ring_start, radius_to = outer_ring_start + width, depth=depth)

p.spindle_off()
p.move(z=20)
p.move(x=0,y=0)
p.end()

with open(args.output_file,'w') as f:
    f.write( p.asText() )
