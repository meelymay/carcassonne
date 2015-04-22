import unittest
import board
from coordinate import *
from tile import *

class BoardTest(unittest.TestCase):

  def test_init(self):
      b = board.Board()
      self.assertEqual(len(b.grid), 1)

  def test_place(self):
      b = board.Board()

      clusters = [
          (CASTLE, [NNW, N, NNE]),
          (ROAD, [W, E]),
          (FARM, [WNW, ENE]),
          (FARM, [WSW, SSW, S, SSE, ESE]),
          (None, [C])
          ]
      t = Tile('foo', clusters)

      c = Coordinate(1, 0)
      b.place(t, c)

      self.assertEqual(len(b.grid), 2)

if __name__ == '__main__':
    unittest.main()
