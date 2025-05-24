from .gcode import GProg,Point
from itertools import count

def make_hole(p, center, r, side, Z, feed, dir='cw'):
    match side:
        case 'left':
            S = center + Point(r,0)
        case 'right':
            S = center - Point(r,0)
        case 'top':
            S = center - Point(0,r)
        case 'bottom':
            S = center + Point(0,r)
        case _:
            raise RuntimeError(f'Invalid side {side}')
    p.move(S)
    for z in Z:
        p.lin(z=z,f=feed)
        p.arc(to=S,center=center,f=feed,dir=dir)

def calc_z(mat_thickness, layer_thickness, bridge_thickness=0):
    tot_depth = mat_thickness - bridge_thickness
    n_layers = int(tot_depth / layer_thickness)
    Z = [layer_thickness * i for i in range(1,n_layers+1)]
    last = tot_depth - layer_thickness*(n_layers)
    if last > 0:
        Z.append( Z[-1] + last if Z else last)
    return [-z for z in Z]

def pads(**kwargs):
    # all units in mm
    tool_dia = kwargs.get('tool_dia',1.5)
    D = kwargs.get('D',10)
    d = kwargs.get('d',4)
    n_pads = kwargs.get('n_pads',4)

    mat_thickness = kwargs.get('mat_thickness',6)
    bridge_thickness = kwargs.get('bridge_thickness',0.2)
    feed = kwargs.get('feed',100)
    layer_thickness = kwargs.get('layer_thickness',1)
    z_safe = kwargs.get('z_safe',5)

    theta = D/2 + tool_dia/2    # outside radius with tool dia correction
    tau = d/2 - tool_dia/2      # insside [hole] radius with tool dia correction

    # O1..O4 pads centers
    # O1 - M1 - O2
    # |         |
    # M4   C    M2
    # |         |
    # O4 - M3 - O3
    C  = Point(x=0,y=0)
    O1 = Point(x=-theta,y= theta)
    O2 = Point(x= theta,y= theta)
    O3 = Point(x= theta,y=-theta)
    O4 = Point(x=-theta,y=-theta)

    M1 = Point(x=0,     y= theta)
    M2 = Point(x=theta, y=     0)
    M3 = Point(x=0,     y=-theta)
    M4 = Point(x=-theta,y=     0)

    p = GProg()
    p.comment(f'{D=} {d=} {tool_dia=} {theta=} {tau=}')
    
    # holes
    Z = calc_z(mat_thickness,layer_thickness)
    Holes = [(O1,'left'), (O2,'right'), (O3,'right'), (O4,'left')]
    for (center,side),i in zip(Holes,count(1)):
        p.comment(f'hole O{i}')
        make_hole(p,center,tau,side,Z,feed)
        p.move(z=z_safe)

    Segments = [(M2,O2),(M3,O3),(M4,O4),(M1,O1)]
    # inside silhouette
    p.comment('inside silhouette')
    p.move(M1,comment='M1')
    
    for z in Z:
        p.lin(z=z,f=feed)
        for to,center in Segments:
            p.arc(to=to,center=center,dir='ccw')
    p.move(z=z_safe)

    # outside silhouette
    Z = calc_z(mat_thickness,layer_thickness,bridge_thickness)
    p.comment('outside silhouette')
    p.move(M1,comment='M1')
    for z in Z:
        p.lin(z=z,f=feed)
        for to,center in Segments:
            p.arc(to=to,center=center,dir='cw')
    p.move(z=z_safe)

    p.spindle_off()
    p.move(C)
    p.end()

    return p.asText()
