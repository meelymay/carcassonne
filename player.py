from meeple import *
from coordinate import *


class Player:

    def __init__(self, name):
        self.name = name
        self.meeples = [Meeple(name) for x in range(7)]

    def score(self):
        return sum([meeple.score for meeple in self.meeples])

    def get_rotations(self):
        # TODO make rotation reading robust
        r = raw_input('Rotations? ')
        return int(r) if r else 0

    def get_coordinate(self):
        # TODO make coordinate reading robust
        x, y = raw_input('Coordinate? ').split()
        return Coordinate(int(x), int(y))

    def get_meeple(self):
        ms = [m for m in self.meeples if not m.placed]
        if ms:
            return ms[0]

    def get_meeple_section(self):
        meeple = self.get_meeple()
        if meeple:
            return raw_input('Meeple section? ')
