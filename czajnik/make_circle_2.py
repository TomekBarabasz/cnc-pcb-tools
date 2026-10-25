import cnc_tools,sys

Pt = cnc_tools.Point
p = cnc_tools.GProg()
#assuming tool at position (0,0)
tr = round(1.5 / 2,2)
center = Pt(0,20)
p.spindle_on()

p.move(to=Pt(0,3*tr))
p.lin(z=-1)
p.arc(to=p.pos, center=center, direction='CW', f=200)
p.lin(x=0,y=tr)
for z in range(-11,-19,-1):
    p.lin(z=z)
    p.arc(to=p.pos, center=center, direction='CW', f=200)

p.lin(x=0,y=0)
p.spindle_off()
p.move(z=20)
p.end()

with open(sys.argv[1],'w') as f:
    f.write( p.asText() )
