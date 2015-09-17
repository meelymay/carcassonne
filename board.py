from deck import *
from coordinate import *


def num_3string(i):
    if i >= 0:
        if abs(i) > 10:
            return str(i)+' '
        else:
            return ' '+str(i)+' '
    else:
        if abs(i) > 10:
            return str(i)
        else:
            return str(i)+' '


def num_5string(i):
    if i == ' ':
        return '     '
    if i >= 0:
        if abs(i) >= 10:
            return ' '+str(i)+'  '
        else:
            return '  '+str(i)+'  '
    else:
        if abs(i) >= 10:
            return ' '+str(i)+' '
        else:
            return ' '+str(i)+'  '


class Board:

    def __init__(self):
        self.deck = Deck()
        self.grid = {Coordinate(0, 0): START_TILE}

    def draw(self):
        return self.deck.draw()

    def get_bounds(self):
        min_x = min([coord.x for coord in self.grid])
        max_x = max([coord.x for coord in self.grid])
        min_y = min([coord.y for coord in self.grid])
        max_y = max([coord.y for coord in self.grid])
        return (min_x, max_x, min_y, max_y)

    def display(self):
        min_x, max_x, min_y, max_y = self.get_bounds()
        board = self

        # width of row numbers
        print '     ',
        # column numbers
        for i in range(min_x, max_x+1):
            print num_5string(i),
        print
        # each row on board
        for y in range(max_y, min_y-1, -1):
            # row number
            for i in range(3):
                if i == 1:
                    print num_5string(y),
                else:
                    print num_5string(' '),
                # each column on board
                for x in range(min_x, max_x+1):
                    c = Coordinate(x, y)
                    if c in board.grid:
                        tmp_tile = board.grid[c]
                        tmp_disp = tmp_tile.displayable()
                        print tmp_disp[i],
                    # empty tile
                    else:
                        print num_5string(' '),
                print

    def can_place(self, tile, coordinate):
        if coordinate in self.grid:
            return False
        neighbors = self.get_neighbors(coordinate)
        if not neighbors:
            return False
        if False in [tile.can_combine(n[0], n[1]) for n in neighbors]:
            return False
        return True

    def place(self, tile, coordinate):
        if not self.can_place(tile, coordinate):
            return False

        for neighbor in self.get_neighbors(coordinate):
            tile.combine_territories(neighbor[0], neighbor[1])
        self.grid[coordinate] = tile
        return True

    def get_neighbors(self, coordinate):
        neighbors = []
        for side in [N, S, E, W]:
            neighbor_coord = coordinate.neighbor(side)
            if neighbor_coord in self.grid:
                neighb_side = (self.grid[neighbor_coord], side)
                neighbors.append(neighb_side)
        return neighbors

    def calculate_scores(self):
        # TODO calculate scores on completed board
        return 0
