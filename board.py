from tiles import *
from deck import *
from coordinate import *
from model import *
from termcolor import cprint, colored

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
        self.grid = {}
        Grid(self.grid)
        self.grid[Coordinate(0,0).val] = start_tile
        start_tile.activate(Coordinate(0,0))
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.deck = Deck()

    def draw(self):
        piece = self.deck.draw()
        while piece and not self.piece_playable(piece):
            piece = self.deck.draw()
        return piece

    def add(self, tile, coordinate):
        if not self.playable(tile, coordinate):
            return False

        self.grid[coordinate.val] = tile
        tile.activate(coordinate)
        for neighbor in self.get_neighbors(coordinate):
            combine_tile_models(tile, neighbor[0], neighbor[1])

        # update dimensions of grid
        self.expand_grid(coordinate.x, coordinate.y)
            
        return True

    def expand_grid(self, x, y):
        if x > self.max_x:
            self.max_x = x
        if x < self.min_x:
            self.min_x = x
        if y > self.max_y:
            self.max_y = y
        if y < self.min_y:
            self.min_y = y

    def playable(self, tile, coordinate):
        if coordinate.val in self.grid or not self.has_adjacent(coordinate):
            return False

        for pos in sides:
            co = coordinate.neighbor(pos).val
            if co in self.grid:
                neighbor = self.grid[co]
                if not neighbor.secs[opp_pos(pos, pos in hor_sides)].connectable(tile.secs[pos]):
                    return False
            else:
                continue
        return True
            
    def get_neighbors(self, coordinate):
        neighbors = []
        for side in sides:
            neighbor_coord = coordinate.neighbor(side).val
            if neighbor_coord in self.grid:
                neighbors.append((self.grid[neighbor_coord], side))
        return neighbors

    def has_adjacent(self, coordinate):
        return len(self.get_neighbors(coordinate)) != 0

    def fitting_pieces(self, coordinate):
        pieces = 0
        for tile in tile_types:
            for i in range(4):
                if self.playable(tile, coordinate):
                    pieces += self.deck.num_left(tile)
                    break
                tile.rotate()
        return pieces

    def piece_playable(self, tile):
        if not tile:
            return False
        playable = False
        for i in range(4):
            for x in range(self.min_x-1, self.max_x+2):
                for y in range(self.min_y-1, self.max_y+2):
                    coordinate = Coordinate(x, y)
                    if self.playable(tile, coordinate):
                        playable = True
                        break
                if playable:
                    break
            if playable:
                break
            tile.rotate()
        return playable

    def display(self):
        # width of row numbers
        print '    ',
        # column numbers
        for i in range(self.min_x, self.max_x+1):
            print num_5string(i),
        print
        # each row on board
        for y in range(self.max_y, self.min_y-1,-1):
            # row number
            for i in range(3):
                if i == 1:
                    print num_5string(y),
                else:
                    print num_5string(' '),
                # each column on board
                for x in range(self.min_x, self.max_x+1):
                    c = Coordinate(x,y) 
                    if c.val in self.grid:
                        tmp_tile = self.grid[c.val]
                        tmp_disp = tmp_tile.displayable()
                        for j in range(3):
                            if tmp_disp[i][j][1] is None:
                                bold = []
                            else:
                                bold = ['bold']
                            cprint(tmp_disp[i][j][0]+' ', 
                                   tmp_disp[i][j][1],
                                   tmp_disp[i][j][2], 
                                   end='',
                                   attrs=bold)
                    # empty tile
                    else:
                        print num_5string(' '),
                print

    def get_grid(self):
        grid = {}

        # width of row numbers
        grid[0] = []
        print '    ',
        # column numbers
        for i in range(self.min_x, self.max_x+1):
            print num_5string(i),
        print
        # each row on board
        for y in range(self.max_y, self.min_y-1,-1):
            # row number
            for i in range(3):
                if i == 1:
                    print num_5string(y),
                else:
                    print num_5string(' '),
                # each column on board
                for x in range(self.min_x, self.max_x+1):
                    c = Coordinate(x,y) 
                    # start tile
                    # if x == 0 and y == 0 and i == 1:
                    #     print '- X -',
                    # other tile
                    if c.val in self.grid:
                        tmp_tile = self.grid[c.val]
                        tmp_disp = tmp_tile.displayable()
                        for j in range(3):
                            if tmp_disp[i][j][1] is None:
                                bold = []
                            else:
                                bold = ['bold']
                            cprint(tmp_disp[i][j][0]+' ', 
                                   tmp_disp[i][j][1],
                                   tmp_disp[i][j][2], 
                                   end='',
                                   attrs=bold)
                        # cprint(tmp_disp[i][2][0]+' ', 
                        #        tmp_disp[i][2][1], 
                        #        tmp_disp[i][2][2],
                        #        end='')
                    # empty tile
                    else:
                        print num_5string(' '),
                print

    def get_model_sections(self):
        models = set([])
        for coord in self.grid:
            tile = self.grid[coord]
            for pos in all_secs:
                section = tile.secs[pos]
                if pos == (0,0) and section.marker != cloister:
                    continue
                models.add(section)
        return models

    def get_models(self):
        model_sections = self.get_model_sections()
        return [m.model for m in model_sections]

    def print_models(self):
        models = self.get_model_sections()

        castles = set([m.model for m in models if m.marker == castle])
        farms = set([m.model for m in models if m.marker == farm])
        roads = set([m.model for m in models if m.marker == road])

        print 'CASTLES:',len(castles)
        for model in castles:
            model.print_model()
        print 'ROADS:',len(roads)
        for model in roads:
            model.print_model()
        print 'FARMS:',len(farms)
        for model in farms:
            model.print_model()

