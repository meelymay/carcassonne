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


class Section:
    
    def __init__(self, tile):
        self.tile = tile
        self.territory = None
        self.meeple = None

    def combine(self, neighbor):
        self.territory.combine(self, neighbor.territory, neighbor)

    def can_combine(self, neighbor):
        return self.territory.name == neighbor.territory.name

    def get_type(self):
        return self.territory.name

    def place_meeple(self, meeple):
        self.meeple = meeple
        meeple.place()

    def replace_meeple(self, score):
        self.meeple.replace(score)
        self.meeple = None

    def __str__(self):
        if not self.territory:
            return ' '
        if self.meeple:
            return self.territory.name.lower()
        else:
            return self.territory.name
