from meeple import *
from coordinate import *
import section


class Player:

    def __init__(self, name):
        self.name = name + ''.join([' ' for i in range(6-len(name))])
        self.meeples = [Meeple(name) for x in range(7)]

    def set_tile(self, tile):
        self.tile = tile

    def score(self):
        return sum([meeple.score for meeple in self.meeples])

    def get_rotations(self):
        while True:
            try:
                r = raw_input('Rotations? ')
                return int(r) if r else 0
            except ValueError:
                continue

    def get_coordinate(self):
        while True:
            try:
                x, y = raw_input('Coordinate? ').split()
                return Coordinate(int(x), int(y))
            except ValueError:
                continue

    def get_meeple(self):
        ms = [m for m in self.meeples if not m.placed]
        if ms:
            return ms[0]

    def get_meeple_section(self):
        while True:
            try:
                meeple = self.get_meeple()
                if meeple:
                    sec = raw_input('Meeple section? ')
                    if sec in section.ALL_SECTIONS + ['']:
                        return sec
                    else:
                        raise KeyError('Section is not a thing.')
                return
            except KeyError:
                continue
