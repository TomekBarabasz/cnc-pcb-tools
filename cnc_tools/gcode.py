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

class GProg:
    def __init__(self, units='mm', coords='abs'):
        self.cmds = []
        self.pos = Point(None,None,None)
        self.units(units).coords(coords)
        
    def units(self, u):
        self.cmds.append( 'G21 (units in mm)' if u=='mm' else 'G20 (units in inches)' )
        return self
    
    def coords(self, c):
        self.cmds.append('G90 (absolute positions)' if c=='abs' else 'G91 (relative positions)')
        self.rel_mode = c=='rel'
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
        cs = GProg._set_feed(cs,kwargs.get('f',None))
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
        cs = GProg._set_feed(cs,kwargs.get('f',None))
        self.cmds.append( CMD[dir] + ' ' + ' '.join(cs))
        return self
