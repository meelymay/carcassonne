from player import *
from ai_player import *
from board import *
from coordinate import *
import time


class Game:

    def __init__(self, strategies, robot=False):
        self.board = Board()
        self.robot = robot
        self.players = [AIPlayer('HAL', self.board, heuristics=strategies[0]),
                        AIPlayer('IBM', self.board, heuristics=strategies[1])]
        self.player = self.players[0]
        self.count = 0
        self.game_over = False
        self.game_len = 72

    def play(self):
        while not self.game_over:
            # time.sleep(1)
            for player in self.players:
                self.player = player
                self.count += 1
                if not self.robot:
                    for p in self.players:
                        print 'Player %s has score \t%s.' % (p, p.score())
                if not self.take_turn():
                    self.game_over = True
                    break
        self.board.calculate_scores()

        winner = max(self.players, key=lambda x: x.score())
        game_dict = {}
        for p in self.players:
            w = ''
            if p == winner:
                w = '<-- WINS!'
            if self.robot:
                game_dict[p.name] = {
                    'strat': p.heuristics,
                    'score': p.score()
                }
            else:
                print 'Player %s has score \t%s. %s' % (p, p.score(), w)
        if self.robot:
            print json.dumps(game_dict)

    def take_turn(self):
        player = self.player
        if not self.robot:
            print "\n------------------\nPlayer %s's turn!" % (player)
            self.board.display()

        # draw a tile
        tile = self.board.draw()
        if tile is None or self.count > self.game_len:
            if not self.robot:
                print 'The game is over.'
            self.game_over = True
            return False
        if not self.robot:
            print 'You drew:'
            tile.display()
        player.set_tile(tile)
        # tile.display_addrs()

        # rotate and place the tile
        placed = None
        while placed is None:
            # rotate the tile
            self.rotate(tile)
            if not self.robot:
                tile.display()
            # place the tile on the board
            placed = self.place(tile)
            if placed is None:
                if not self.robot:
                    print 'Tile cannot placed there.'

        # add a meeple
        meeple = player.get_meeple()
        # while meeple:
        if meeple:
            meeple = self.add_meeple(tile, meeple)

        # score
        tile.score()
        # check for finished cloisters
        for neighbor in self.board.get_all_neighbors(placed):
            neighbor.score()

        return True

    def rotate(self, tile):
        rotations = self.player.get_rotations()
        tile.rotate_n(rotations)

    def place(self, tile):
        coordinate = self.player.get_coordinate()
        return self.board.place(tile, coordinate)

    def add_meeple(self, tile, meeple):
        section = self.player.get_meeple_section()
        if section:
            if not tile.place_meeple(section, meeple):
                return meeple

if __name__ == '__main__':
    g = Game([HEURISTICS, HEURISTICS], robot=True)
    g.play()
