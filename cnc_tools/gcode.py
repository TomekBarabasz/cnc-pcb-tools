from math import ceil, hypot

class Point:
    def __init__(self, x,y,z=None):
        self.x = x
        self.y = y
        self.z = z
    def set(self, x,y,z):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z
    def __add__(self, other):
        if self.z is None and other.z is None:
            z = None
        elif self.z is not None and other.z is not None:
            z = self.z + other.z
        else:
            raise RuntimeError('unmatched z coords')
        return Point(self.x + other.x, self.y + other.y, z)
    def __sub__(self, other):
        if self.z is None and other.z is None:
            z = None
        elif self.z is not None and other.z is not None:
            z = self.z - other.z
        else:
            raise RuntimeError('unmatched z coords')
        return Point(self.x - other.x, self.y - other.y, z)
    def __mul__(self, scalar):
        return Point(self.x * scalar if self.x is not None else None, 
                     self.y * scalar if self.y is not None else None, 
                     self.z * scalar if self.z is not None else None)
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    def __truediv__(self, scalar):
        return Point(self.x / scalar if self.x is not None else None, 
                     self.y / scalar if self.y is not None else None, 
                     self.z / scalar if self.z is not None else None)
    def normalize(self):
        length = hypot(self.x, self.y)
        if length == 0:
            raise RuntimeError('Cannot normalize zero-length vector')
        return self / length
    def nearest_point_on_circle(self, center, radius):
        # Direction vector
        dx,dy = self.x - center.x, self.y - center.y
        distance = hypot(dx, dy)
        
        # Handle special case
        if distance == 0:
            return Point(center.x + radius, center.y)
        
        return center + Point(dx, dy) / distance * radius

class GProg:
    def __init__(self, units='mm', coords='abs'):
        self.cmds = []
        self.pos = Point(None,None,None)
        self.units(units).coords(coords)
        self._feed_rate = None
        self._tool_dia = None
        self._tool_overlap_mm = None
        self._z_travel = 10
        
    def units(self, u):
        self.cmds.append( 'G21 (units in mm)' if u=='mm' else 'G20 (units in inches)' )
        return self
    
    def coords(self, c):
        self.cmds.append('G90 (absolute positions)' if c=='abs' else 'G91 (relative positions)')
        self.rel_mode = c=='rel'
        return self

    def feed_rate(self, fr):
        self._feed_rate = fr
        return self
    
    def tool_dia(self, td):
        self._tool_dia = td
        return self
    
    def get_tool_radius(self):
        assert(self._tool_dia is not None)
        return round(self._tool_dia / 2, 2)
    
    def tool_overlap(self, **kwargs):
        if 'mm' in kwargs:
            self._tool_overlap_mm = kwargs['mm']
        elif 'pct' in kwargs:
            assert(self.tool_dia is not None)
            self._tool_overlap_mm = self.tool_dia * kwargs['pct'] / 100
        else:
            raise RuntimeError('set_tool_overlap requires mm= or pct=')
        return self
    
    def z_travel(self, zt):
        self._z_travel = zt
        return self
    
    def change_tool(self, tool_dia_, **kwargs):
        cur_pos = self.pos
        self.move(to=None, **kwargs)
        self.cmds.append( "M0" )
        self.cmds.append( "M06" )
        self.move(to=cur_pos)
        self.tool_dia(tool_dia_)
        return self
    
    def _move_coords(self, to, **kwargs):
        coords = (to.x,to.y,to.z) if to is not None else tuple(kwargs.get(n,None) for n in 'xyz')
        if self.rel_mode:
            self.pos += Point(*coords)
        else:
            self.pos.set(*coords)
        return [n+str(c) for n,c in zip('XYZ',coords) if c is not None]
    
    def move(self, to=None, **kwargs):
        cs = self._move_coords(to,**kwargs)
        if (len(cs)==0):
            return self
        comment = kwargs.get('comment',None)
        if comment is not None:
            cs.append(f'({comment})')
        self.cmds.append( 'G00 ' + ' '.join(cs))
        return self
    
    @staticmethod
    def _set_feed(cs, feed):
        return cs + [f'F{feed}'] if feed is not None else cs

    def lin(self, to=None, **kwargs):
        cs = self._move_coords(to,**kwargs)
        cs = GProg._set_feed(cs,kwargs.get('f',self._feed_rate))
        self.cmds.append( 'G01 ' + ' '.join(cs))
        return self
    
    def asText(self):
        return '\n'.join(self.cmds)
    def end(self):
        self.cmds.append('M30')
    def spindle_on(self):
        self.cmds.append('M03')
        return self
    def spindle_off(self):
        self.cmds.append('M05')
        return self
    def comment(self, text): 
        self.cmds.append( f'({text})')
        return self

    def arc(self, to, center=None, **kwargs):
        dir = kwargs.get('dir','cw')
        CMD = {'cw':'G02','ccw':'G03'}
        if center is not None:
            ij = (center.x - self.pos.x, center.y - self.pos.y)
        else:
            ij = tuple(kwargs.get(n,None) for n in ['cox','coy'])
        cs = self._move_coords(to,**kwargs)
        cs += [n+str(v) for n,v in zip('IJ',ij) if v is not None]
        cs = GProg._set_feed(cs,kwargs.get('f',self._feed_rate))
        self.cmds.append( CMD[dir] + ' ' + ' '.join(cs))
        return self

    @staticmethod
    def _make_depth_table(depth):
        if isinstance(depth, range):
            depth_table = list(depth)
        elif isinstance(depth, (float, int)):
            depth_table = [depth]
        elif isinstance(depth, list):
            depth_table = depth
        else:
            raise RuntimeError('depth must be range or float/int')
        return depth_table

    def line(self, start, end, depth, **kwargs):
        feed = kwargs.get('f',self._feed_rate)
        z_travel = kwargs.get('z_travel',self._z_travel)
        self.move(z=z_travel)
        self.move(to=start)
        depth_table = GProg._make_depth_table(depth)
        dir = 1 # 1 : from start to end
        for i in range(len(depth_table)):
            self.lin(z=depth_table[i], f=feed)
            self.lin(to=end if dir else start, f=feed)
            dir = 1 - dir
        
        self.move(z=z_travel)
        def get_endpoint(kwargs):
            end_point = kwargs.get('end_point',None)
            if end_point is not None:
                if isinstance(end_point, Point):
                    return end_point
                else:
                    match end_point:
                        case 'start':
                            return start
                        case 'end':
                            return end
                        case _:
                            raise RuntimeError('end_point must be "start" or "end"')
            return None
        self.move( get_endpoint(kwargs) )
        return self

    def circle(self, center, radius, depth, **kwargs):
        z_travel = kwargs.get('z_travel',self._z_travel)
        feed = kwargs.get('f',self._feed_rate)
        nearest = self.pos.nearest_point_on_circle(center, radius)
        self.move(z=z_travel)
        self.move(to=nearest)
        depth_table = GProg._make_depth_table(depth)
        for z in depth_table:
            self.lin(z=z, f=feed)
            self.arc(to=self.pos, center=center, **kwargs)
        self.move(z=z_travel)
        return self
    
    def cylinder(self, center, radius, depth, **kwargs):
        feed = kwargs.get('f',self._feed_rate)
        tool_overlap_mm = kwargs.get('tool_overlap_mm',self._tool_overlap_mm)
        z_travel = kwargs.get('z_travel',self._z_travel)
        depth_table = GProg._make_depth_table(depth)
        self.move(z=z_travel)
        self.move(to=center)
        # initial hole
        self.lin(z=depth_table[-1], f=feed)
        self.move(z=0)
        nsteps = ceil( (radius - self.get_tool_radius()) / tool_overlap_mm )
        step = (radius - self.get_tool_radius()) / nsteps
        for z in depth_table:
            self.lin(z=z, f=feed)
            for _ in range(nsteps):
                self.lin(x=self.pos.x + step)
                self.arc(to=self.pos, center=center, **kwargs)
            self.move(to=center)
        self.move(z=z_travel)
        return self
    
    def ring(self, center, radius_from, radius_to, depth, **kwargs):
        feed = kwargs.get('f',self._feed_rate)
        tool_overlap_mm = kwargs.get('tool_overlap_mm',self._tool_overlap_mm)
        z_travel = kwargs.get('z_travel',self._z_travel)
        depth_table = GProg._make_depth_table(depth)
        tr = self.get_tool_radius()
        nearest = self.pos.nearest_point_on_circle(center, radius_from + tr)
        self.move(z=z_travel)
        self.move(to=nearest)
        nsteps = ceil( (radius_to - radius_from - tr) / tool_overlap_mm )
        step = (radius_to - radius_from - tr) / nsteps
        step_dir = (nearest - center).normalize()
        for z in depth_table:
            self.lin(z=z, f=feed)
            for _ in range(nsteps):
                self.arc(to=self.pos, center=center, **kwargs)
                self.lin(to=center + step_dir * step)
            self.arc(to=self.pos, center=center, **kwargs)
            self.move(to=nearest)
        self.move(z=z_travel)
        return self