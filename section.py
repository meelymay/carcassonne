WNW = 'WNW'
NNW = 'NNW'
N = 'N'
NNE = 'NNE'
ENE = 'ENE'
W = 'W'
C = 'C'
E = 'E'
WSW = 'WSW'
SSW = 'SSW'
S = 'S'
SSE = 'SSE'
ESE = 'ESE'

OPPOSING_DIRECTION = {
    WNW: ENE,
    NNW: SSW,
    N: S,
    NNE: SSE,
    ENE: WNW,
    W: E,
    C: C,
    ESE: WSW,
    SSW: NNW,
    S: N,
    SSE: NNE,
    WSW: ESE,
    E: W
}

FULL_SIDE = {
    N: [NNW, NNE, N],
    W: [W, WNW, WSW],
    E: [ESE, E, ENE],
    S: [SSW, S, SSE]
}

ALL_SIDES = FULL_SIDE[W] + FULL_SIDE[N] + FULL_SIDE[E] + FULL_SIDE[S]
ALL_SECTIONS = ALL_SIDES + [C]


COLORS = {
    'c': '\033[41m',
    'r': '\033[47m',
    'f': '\033[42m',
    'l': '\033[45m'
}

ENDC = '\033[0m'
MEEPLE = '\033[36m\033[1m'


class Section:

    def __init__(self, tile):
        self.tile = tile
        self.territory = None
        self.meeple = None
        self.id = str([self])[-7:-2]

    def combine(self, neighbor):
        self.territory.combine(self, neighbor.territory, neighbor)
        neighbor.territory = self.territory

    def can_combine(self, neighbor):
        return self.territory.name == neighbor.territory.name

    def get_type(self):
        return self.territory.name

    def place_meeple(self, meeple):
        if self.territory.get_meeples():
            return False
        self.meeple = meeple
        meeple.place()
        return True

    def replace_meeple(self, score):
        self.meeple.replace(score)
        self.meeple = None

    def addr(self):
        return self.id

    def __str__(self):
        if not self.territory:
            return ' '
        name = self.territory.name
        if self.meeple:
            return COLORS[name.lower()] + self.meeple.color + '#' + ENDC
        else:
            return COLORS[name.lower()] + ' ' + ENDC
