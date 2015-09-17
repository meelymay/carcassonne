from player import *
from ai_player import *
from board import *
from coordinate import *
import time


class Game:

    def __init__(self, names):
        self.board = Board()
        self.players = [AIPlayer('IBM', self.board), AIPlayer('HAL', self.board)]
        self.player = self.players[0]
        self.count = 0
        self.game_over = False
        self.game_len = 72

    def play(self):
        while not self.game_over:
            time.sleep(1)
            for player in self.players:
                self.player = player
                self.count += 1
                if not self.take_turn():
                    self.game_over = True
                    break
                for p in self.players:
                    print 'Player %s has score \t%s.' % (p.name, p.score())
        self.board.calculate_scores()

    def take_turn(self):
        player = self.player
        print "\n------------------\nPlayer %s's turn!" % (player.name)
        self.board.display()

        # draw a tile
        tile = self.board.draw()
        if tile is None or self.count > self.game_len:
            print 'The game is over.'
            self.game_over = True
            return False
        print 'You drew:'
        tile.display()
        player.set_tile(tile)
        # tile.display_addrs()

        # rotate and place the tile
        placed = False
        while not placed:
            # rotate the tile
            self.rotate(tile)
            tile.display()
            # place the tile on the board
            placed = self.place(tile)
            if not placed:
                print 'Tile cannot placed there.'

        # add a meeple
        meeple = player.get_meeple()
        # while meeple:
        if meeple:
            meeple = self.add_meeple(tile, meeple)

        # score
        tile.score()

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
    g = Game(['Amelia', 'Dan'])
    g.play()
