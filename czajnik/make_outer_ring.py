import cnc_tools,sys
from math import ceil

tool_dia = float(sys.argv[2]) if len(sys.argv)>2 else 1.5
tool_radius = round(tool_dia/2, 2)
tool_overlap = round(tool_dia * 2/3, 2)
Pt = cnc_tools.Point
p = cnc_tools.GProg()

center = Pt(0,0)
p.move(to=center)
p.spindle_on()
p.set_feed_rate(200)
p.comment("outer ring")
outer_ring_pos = 13.5 + 5.2
p.move(x=outer_ring_pos,y=0)
for z in range(-1,-19,-1):
    p.lin(z=z)
    p.arc(to=p.pos, center=center, direction='CW')
p.move(z=0)

p.spindle_off()
p.move(z=20)
p.move(x=0,y=0)
p.end()

with open(sys.argv[1],'w') as f:
    f.write( p.asText() )
