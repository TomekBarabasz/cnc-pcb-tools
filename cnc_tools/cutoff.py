import math
from .gcode import GCode

def calc_cut_width(job):
    match job.tool.shape:
        case 'c' | 'circle':
            return job.tool.diameter
        case 'v':
            return 2 * math.sin(job.tool.angle) * job.cut.layer
        case _:
            print('error: unsupported tool shape :', job.tool.shape)
            exit(1)

def cutoff(job):
    cut_depth_total = job.cut.depth
    cut_depth_layer = job.cut.layer
    cut_feed  = job.cut.feed
    cut_zfeed = job.cut.zfeed
    cut_width = calc_cut_width(job)
    x0,y0 = list(map(float,job.geometry.origin.split(','))) if hasattr(job.geometry,'origin') else [0,0]
    x = x0 - cut_width/2
    y = y0 - cut_width/2
    z = -cut_depth_layer
    commands = GCode.start()
    commands += GCode.spindle_off()
    commands += GCode.move_to(x=x0,y=y0)
    commands += GCode.spindle_on()
    n_layers = int(math.ceil(cut_depth_total / cut_depth_layer))
    while n_layers > 0:
        commands += GCode.linear(z=z,f=cut_zfeed)
        x += job.geometry.width + cut_width
        commands += GCode.linear(x=x,f=cut_feed)
        y += job.geometry.height + cut_width
        commands += GCode.linear(y=y)
        x = x0 - cut_width/2
        commands += GCode.linear(x=x)
        y = y0 - cut_width/2
        commands += GCode.linear(y=y)
        z = max(z-cut_depth_layer,-cut_depth_total)
        n_layers = n_layers - 1
    commands += GCode.move_to(z=job.tool.zmoving)
    commands += GCode.spindle_off()
    commands += GCode.move_to(x=0,y=0)
    commands += GCode.end()
    return commands
