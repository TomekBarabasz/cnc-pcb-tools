from cnc_tools.svg import parse_svg_path,read_svg_paths,flatten_bezier,poly_to_toolpath
import matplotlib.pyplot as plt
import sys
from cnc_tools.svg.common import midpoint, perpendicular, normalize
import sys
from pathlib import Path

test_num = int(sys.argv[1]) if len(sys.argv) > 1 else 0

if test_num == 0:
    plt.figure(figsize=(6, 8))

    sq = [( (0,0), (0,2) ),
        ( (0,2), (2,2) ), 
        ( (2,2), (2,0) ), 
        ( (2,0), (0,0) ) ]

    O,L = zip(*sq)
    print(O)
    L = [(u-x,v-y) for (x,y),(u,v) in sq]
    print(L)
    ox,oy = zip(*O)
    u,v = zip(*L)
    plt.quiver(ox,oy, u,v, angles='xy', scale_units='xy', scale=1)

    #M = [midpoint(*e) for e in sq]
    M = [e[0] for e in sq]
    N = map(perpendicular, L)
    N = map(normalize, N)
    ox,oy = zip(*M)
    u,v = zip(*N)
    plt.quiver(ox, oy, u,v, angles='xy', scale_units='xy', scale=1, color='red')
    plt.xlim(-3,3)
    plt.ylim(-3,3)
    plt.show()
    exit(0)

if test_num == 1:
    lines = [ (0,0), (0,2), (2,2), (2,0) ]
    outset, normals  = poly_to_toolpath(lines, tool_radius=.2, outward=True, closed=True)
    x,y = zip(*lines)
    plt.plot(x, y, label='figure', color='blue')

    x,y = zip(*outset)
    plt.plot(x, y, label='toolpath', color='red')

    O,N = zip(*normals)
    ox,oy = zip(*O)
    u,v = zip(*N)
    plt.quiver(ox,oy, u,v, angles='xy', scale_units='xy', scale=1, color='red')
    plt.xlim(-3,3)
    plt.ylim(-3,3)
    plt.show()
    exit(0)

if test_num == 2:
    p = Path(r"C:\tomek\cnc\visiorek.svg")
    if p.exists():
        Paths = read_svg_paths(str(p))
        print(','.join(Paths.keys()))
        curves = parse_svg_path(Paths['path11'])
    else:
        curves = parse_svg_path("M 18.305942,11.739082 C 19.377937,16.46014 15.440135,25.154584 10.185389,30.233537 4.184859,24.854689 1.0356561,17.18134 1.2145156,10.421087 1.3933752,3.6608348 5.4841605,1.1100861 10.142875,1.1100861 c 4.658715,0 6.504945,3.1763541 6.504945,6.4624299 0,3.286077 -1.975106,4.889339 -4.209084,4.889339 -2.233978,0 -3.4029644,-0.272006 -3.9965028,-2.33838 -0.2121747,-2.5175536 1.2329631,-3.1886987 1.2329631,-3.1886987 0,0 -0.010115,2.5934755 1.8281877,2.5509597 1.838322,-0.042516 1.913222,-1.4282141 1.913222,-2.5509597 0,-1.122746 -0.934122,-2.4234115 -3.868956,-2.4234115 -2.934833,0 -4.6767591,3.2675769 -4.6767591,5.6971422 0,2.429566 2.0802103,5.314498 5.3144971,5.314498 3.234288,0 5.935989,-0.924155 8.120554,-3.783923 z")

    precision_mm = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    lines = []
    for b in curves:
        lines += b.flatten(precision_mm)

    plt.figure(figsize=(6, 8))

    x,y = zip(*[p.toTuple() for p in lines])
    plt.plot(x, y, label='Flattened Bézier', color='blue')
    plt.show()
    exit(0)

    outset, normals  = poly_to_toolpath(lines, tool_radius=1.0, outward=True, closed=True)

    #x,y = zip(*outset)
    #plt.plot(x, y, label='toolpath', color='red')

    O,L = zip(*normals)
    ox,oy = zip(*O)
    u,v = zip(*L)
    plt.quiver(ox,oy, u,v, angles='xy', scale_units='xy', scale=1)
    plt.show()
    exit(0)
