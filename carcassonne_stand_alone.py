import sys
from board import *
from coordinate import *
from protocol import *
from termcolor import cprint, colored

colors = ['magenta','cyan','blue','yellow']

class Meeple:
    def __init__(self, player):
        self.player = player
        self.section = None
        self.color = player.get_color()

    def set_section(self, section):
        self.section = section

    def repossess(self, score):
        self.player.add_score(score)
        self.section = None

    def is_available(self):
        return self.section is None

    def displayable(self):
        if self.section is None:
            return self,self.player, self.section
        else:
            return self,self.player,self.section.displayable()
    
    def get_color(self):
        return self.player.get_color()

class Player:
    
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.color = colors.pop()
        self.meeples = [Meeple(self) for m in range(7)]

    def get_meeple(self):
        for meeple in self.meeples:
            if meeple.is_available():
                return meeple
        return None

    def num_meeples(self):
        mps = 0
        for meeple in self.meeples:
            if meeple.is_available():
                mps += 1
        return mps

    def add_score(self, score):
        self.score += score

    def get_color(self):
        return self.color

class Game:
    
    def __init__(self, num_players, names=[]):
        if len(names) == 0:
            for p in range(num_players):
                name = 'Player'+str(p+1)
                names.append(name)
        self.board = Board()
        self.players = [Player(names[p]) for p in range(num_players)]
    
    def play(self):
        game_over = False
        game_len = 72
        count = 0
        while not game_over:
            count += 1
            for player in self.players:

                # show the board
                #self.board.display()
                sb = SerialGrid(self.board, player.name)
                sb.print_grid()
                # self.board.print_models()
                
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
                for model in self.board.get_models():
                    model.return_meeples()
        self.calculate_scores()

    def calculate_scores(self):
        for model in self.board.get_models():
            model.score_meeples()

        for player in self.players:
            print '\n',player.name,"'s score:",player.score

    def rotate(self, tile):
        try:
            i = raw_input('How many clockwise rotations would you like to do? ')
            if len(i) == 0:
                # don't rotate
                rotations = 0
                return rotations
            else:
                rotations = int(i)
                tile.rotate_n(rotations)
                # display tile
                tile.display()
                return rotations
        except:
            print 'That is not a valid number of rotations.'
            if i == 'EXIT':
                sys.exit()

    def place(self, tile):
        try:
            coord_string = raw_input('Where would you like to place the tile? ')
            coord = [int(i) for i in coord_string.split()]
            # try adding to board
            added = self.board.add(tile, Coordinate(coord[0], coord[1]))
            if not added:
                print 'You cannot place the tile there.'
                return False
            return True
        except:
            print 'That is not a valid coordinate.'
            if coord_string == 'EXIT':
                sys.exit()
            return False

    def add_meeple(self, tile, meeple):
        try:
            coord_string = raw_input('Which section of your tile would you like to place the meeple? ')
            if len(coord_string) == 0 or \
                    coord_string.lower().strip() == 'none':
                return None
            
            position = tuple([int(i) for i in coord_string.split()])
            if position not in all_out_secs:
                if 'cloister' in tile.name:
                    return tile.add_meeple(position, meeple)
                else:
                    print 'The meeple must be on one of the outside sections.'
                    return meeple
            return tile.add_meeple(position, meeple)

        except:
            print 'That is not a valid section for the meeple.'
            if coord_string == 'EXIT':
                sys.exit()
            return meeple
        

if __name__ == '__main__':
    g = Game(2, ['Amelia','Andy'])
    g.play()
