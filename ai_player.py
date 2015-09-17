from player import *
from coordinate import *
from section import *


class Play:
    def __init__(self, rotations, coordinate):
        self.rotations = rotations
        self.coordinate = coordinate

    def __hash__(self):
        return self.rotations.__hash__() + self.coordinate.__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


class AIPlayer(Player):
    def __init__(self, name, board):
        self.board = board
        Player.__init__(self, name)

    def get_fit(self, coordinate):
        neighbors = self.board.get_neighbors(coordinate)
        fit = len(neighbors)

        # TODO find neighbors with my territory

        # TODO consider how many potential tiles there are left that could fill that spot

        return fit

    def set_tile(self, tile):
        self.tile = tile.copy()
        board = self.board

        found = False
        possibilities = {}
        for rotation in range(4):
            if found:
                break
            self.rotations = rotation
            if rotation:
                self.tile.rotate()
            min_x, max_x, min_y, max_y = board.get_bounds()
            for x in range(min_x-1, max_x+2):
                if found:
                    break
                for y in range(min_y-1, max_y+2):
                    c = Coordinate(x, y)
                    if board.can_place(self.tile, c):
                        self.coordinate = c
                        possibilities[Play(rotation, c)] = self.get_fit(self.coordinate)
                        # found = True
                        # break

        play = max(possibilities, key=lambda x: possibilities[x])
        self.rotations = play.rotations
        self.coordinate = play.coordinate

        self.meeple_section = ''
        self.tile = tile.copy()
        self.tile.rotate_n(self.rotations)
        secs = self.tile.sections
        for sec in secs:
            if secs[sec].territory.name == 'C':
                self.meeple_section = sec
                break

    def get_rotations(self):
        return self.rotations

    def get_coordinate(self):
        return self.coordinate

    def get_meeple_section(self):
        return self.meeple_section
