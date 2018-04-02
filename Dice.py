class Dice:
    '''
    this class emulates a six sided dice with numbers 1 to 6 on each side such that the sum of numbers on two
    opposite sides is always 1.
    '''
    __slots__ = 't', 'd', 'l', 'r', 'f', 'b'

    def __init__(self):
        self.t = 1
        self.d = 6
        self.l = 4
        self.r = 3
        self.f = 5
        self.b = 2

    def __eq__(self, other):
        return self.t == other.t and self.f == other.f

    def __str__(self):
        # north/ up = back, right/ east = right
        return "Die Orientation: Top = {}  North = {} East = {}".format(self.t, self.b, self.r)

    def __repr__(self):
        return str(self)
