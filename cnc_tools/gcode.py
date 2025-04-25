class GCode:
    @staticmethod
    def start():   return ['G21 (units in mm)','G90 (absolute positions)']
    @staticmethod
    def spindle_on():  return ['M03']
    @staticmethod
    def spindle_off(): return ['M05']
    @staticmethod
    def end(): return ['M30']
    @staticmethod
    def comment(text): return [f'({text})']
    @staticmethod
    def feed_rate(fr): return [f'F{fr}']
    @staticmethod
    def _coords(**kwargs):
        c = ''
        if 'x' in kwargs: c += f" X{kwargs['x']}"
        if 'y' in kwargs: c += f" Y{kwargs['y']}"
        if 'z' in kwargs: c += f" Z{kwargs['z']}"
        return c
    @staticmethod
    def move_to(**kwargs):
        return ['G00 ' + GCode._coords(**kwargs)]
    @staticmethod
    def linear(**kwargs):
        c = 'G01 ' + GCode._coords(**kwargs)
        if 'f' in kwargs: c += f" F{kwargs['f']}"
        return [c]
    @staticmethod
    def circular(**kwargs):
        pass
    @staticmethod
    def circular_ccw(**kwargs):
        pass
