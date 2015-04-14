import json
from termcolor import cprint, colored
from coordinate import *

errors = ['You cannot rotate that tile.',
          'You cannot place that tile there.',
          'You have no more meeples.',
          'You cannot place a meeple there.',
          'Bad request.',
          'It is not your turn!',
          'Game has not started yet.',
          'GAME OVER']

def num_5char_arr(i):
    if i == ' ':
        s = '      '
    elif i >= 0:
        if abs(i) >= 10:
            s = '  '+str(i)+'  '
        else:
            s = '   '+str(i)+'  '
    else:
        if abs(i) >= 10:
            s = '  '+str(i)+' '
        else:
            s = '  '+str(i)+'  '
    return [(x,None,None) for x in s]

# class Move:

#     def __init__(self, rotations, position, meeple_section):
#         self.rotations = rotations
#         self.position = position
#         self.meeple_section = meeple_section

#     def serialize(self):
#         return json.dumps({"rotations": self.rotations,
#                            "position": self.position,
#                            "meeple_section": self.meeple_section})
        
#     @classmethod
#     def create_move(cls, json_move):
#         move = json.loads(json_move)
#         return Move(move["rotations"],
#                     move["position"],
#                     move["meeple_section"])

class SerialGrid:

    # grid{y_min:{'x_min':(marker, color, on_color),
    #             ...
    #             'x_max':(marker, color, on_color),},
    #      ...
    #      y_max:{'x_min':(marker, color, on_color),
    #             ...
    #             'x_max':(marker, color, on_color),p}}

    def __init__(self, board, player):
        self.player = player
        if board is None:
            self.grid = None
            return

        grid = []
        grid.append([])
        # width of row numbers
        for i in range(5):
            char = (' ',None, None)
            grid[0].append(char)
        # column numbers
        for i in range(board.min_x, board.max_x+1):
            grid[0] += num_5char_arr(i)

        grid_y = 0
        grid_x = 0
        # each row on board
        for y in range(board.max_y, board.min_y-1,-1):
            # row number
            for i in range(3):
                grid.append([])
                grid_y += 1
                if i == 1:
                    grid[grid_y] += num_5char_arr(y)
                    grid_x += 5
                else:
                    grid[grid_y] += num_5char_arr(' ')
                    grid_x += 5
                # each column on board
                for x in range(board.min_x, board.max_x+1):
                    c = Coordinate(x,y) 
                    if c.val in board.grid:
                        tmp_tile = board.grid[c.val]
                        tmp_disp = tmp_tile.displayable()
                        for j in range(3):
                            grid[grid_y].append(tmp_disp[i][j])
                            grid[grid_y].append((' ',
                                                 tmp_disp[i][j][1],
                                                 tmp_disp[i][j][2]))
                    # empty tile
                    else:
                        grid[grid_y] += num_5char_arr(' ')
                        grid_x += 5
        self.grid = grid

    def serialize(self):
        return json.dumps({'grid': self.grid,
                           'player': self.player})
        
    def print_grid(self):
        for row in self.grid:
            for c in row:
                if c[1] is None:
                    bold = []
                else:
                    bold = ['bold']
                cprint(c[0],c[1],c[2],end='',attrs=bold)
            print

    @classmethod
    def create_grid(cls, json_grid):
        d = json.loads(json_grid)
        sg = SerialGrid(None, 'dummy')
        sg.grid = d['grid']
        sg.player = d['player']
        return sg

class StartTurn:

    def __init__(self, color, meeples, score, tile):
        self.color = color
        self.meeples = meeples
        self.score = score
        self.tile = tile

    def serialize(self):
        d = {}
        d['color'] = self.color
        d['meeples'] = self.meeples
        d['score'] = self.score
        d['tile'] = self.tile
        return json.dumps(d)

    def print_tile(self):
        SerialGrid.create_grid(json.dumps({'grid': self.tile,
                                           'player': 'dummy'})).print_grid()

    @classmethod
    def create_turn(cls, turn):
        d = json.loads(turn)
        return StartTurn(d['color'],
                         d['meeples'],
                         d['score'],
                         d['tile'])
