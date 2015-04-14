import sys
from player import *
from board import *
from coordinate import *
from protocol import *
from termcolor import cprint, colored

class Game:
    
    def __init__(self, names=[]):
        if len(names) == 0:
            for p in range(num_players):
                name = 'Player'+str(p+1)
                names.append(name)
        self.board = Board()
        self.players = [Player(name) for name in names]
        self.player = self.players[0]
        self.tile = None
    
    def draw(self):
        self.tile = self.board.draw()
        if self.tile is None:
            print 'The game is over.'
            game_over = True
            return None

        return self.tile.gridify()

    def play(self):
        game_over = False
        game_len = 72
        count = 0
        while not game_over:
            count += 1
            for player in self.players:

                # show the board
                sb = SerialGrid(self.board, player.name)
                sb.print_grid()
                
                # draw a tile
                tile = self.board.draw()
                if tile is None or count > game_len:
                    print 'The game is over.'
                    game_over = True
                    break

                cprint('\n'+player.name+"'s turn",player.color)
                print '\tmeeples:',player.num_meeples(),
                print '\tscore:',player.score
                print 'You have drawn:'
                tile.display()
                
                # rotate and place the tile
                placed = False
                while not placed:
                    # rotate the tile
                    self.rotate(tile)
                    # place the tile on the board
                    placed = self.place(tile)
                    
                # add a meeple
                meeple = player.get_meeple()
                while meeple:
                    meeple = self.add_meeple(tile, meeple)

                # return meeples
                self.return_meeples()
        self.calculate_scores()

    def return_meeples(self):
        for model in self.board.get_models():
            model.return_meeples()

    def next_player(self):
        next_index = (self.players.index(self.player)+1) % len(self.players)
        self.player = self.players[next_index]

    def calculate_scores(self):
        for model in self.board.get_models():
            model.score_meeples()

        for player in self.players:
            print '\n',player.name,"'s score:",player.score

    def rotate(self, tile, rotations=1):
        tile.rotate_n(rotations)
        return tile.gridify()

    def place(self, tile, position):
        added = self.board.add(tile,
                               Coordinate(position[0], 
                                          position[1]))
        if not added:
            return False
        return True

    def add_meeple(self, position):
        meeple = self.player.get_meeple()
        if meeple is None:
            print 'Meeple DNE!'
            sys.exit()
        if True:
        #try:
            print 'meeple position',position
            if tuple(position) not in all_out_secs:
                if 'cloister' in self.tile.name:
                    tile_add = self.tile.add_meeple(position, meeple)
                    print 'meeple cloister',tile_add
                    return tile_add is None
                else:
                    return False
            added = self.tile.add_meeple(position, meeple)
            print 'meeple added',added
            return added is None

        # except:
        #     print 'meeple exception'
        #     return False
        
