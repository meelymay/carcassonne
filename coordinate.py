from section import *

DIRECTIONS = {
    N: (0, 1),
    W: (-1, 0),
    S: (0, -1),
    E: (1, 0)
}


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def coord_from_val(val):
        return Coordinate(val % 1000,
                          val / 1000)

    def neighbor(self, dir):
        pos = DIRECTIONS[dir]
        return Coordinate(self.x+pos[0], self.y+pos[1])

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __hash__(self):
        return self.x + 1000*self.y

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
