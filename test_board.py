import unittest
import board
from coordinate import *
from tile import *

DEFAULT_CLUSTERS = [
    (CASTLE, [NNW, N, NNE]),
    (ROAD, [W, E]),
    (FARM, [WNW, ENE]),
    (FARM, [WSW, SSW, S, SSE, ESE]),
    (FARM, [C])
]

DEFAULT_TILE = Tile('default', DEFAULT_CLUSTERS)


class BoardTest(unittest.TestCase):

    def test_init(self):
        b = board.Board()
        self.assertEqual(len(b.grid), 1)

    def test_place(self):
        b = board.Board()

        c = Coordinate(1, 0)
        b.place(DEFAULT_TILE, c)

        self.assertEqual(len(b.grid), 2)

    def test_place_existing(self):
        b = board.Board()
        c = Coordinate(0, 0)
        placed = b.place(DEFAULT_TILE, c)
        self.assertFalse(placed)

        b.place(DEFAULT_TILE, Coordinate(1, 0))
        placed = b.place(DEFAULT_TILE, Coordinate(1, 0))
        self.assertFalse(placed)

    def test_place_space(self):
        b = board.Board()
        c = Coordinate(1, 1)
        self.assertFalse(b.place(DEFAULT_TILE, c))

    def test_place_mismatch(self):
        b = board.Board()
        c = Coordinate(0, 1)
        self.assertFalse(b.place(DEFAULT_TILE, c))

if __name__ == '__main__':
    unittest.main()
