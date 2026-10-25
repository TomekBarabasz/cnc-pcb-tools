import cnc_tools,sys

Pt = cnc_tools.Point
p = cnc_tools.GProg()
#assuming tool at position (0,0)
tr = round(1.5 / 2,2)
p.move(to=Pt(0,0))
p.spindle_on()
center = Pt(0,20)
for z in range(-1,-11,-1):
    p.lin(z=z)
    p.arc(to=p.pos, center=center, direction='CW', f=200)
    p.lin(y=p.pos.y + tr)
    p.arc(to=p.pos, center=center, direction='CW', f=200)
    p.lin(y=p.pos.y + tr)
    p.arc(to=p.pos, center=center, direction='CW', f=200)
    p.lin(x=0,y=0)

p.spindle_off()
p.end()

with open(sys.argv[1],'w') as f:
    f.write( p.asText() )
