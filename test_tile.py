import unittest
import tile
from territory import *
from section import *

class TileTest(unittest.TestCase):

  def test_init(self):
      clusters = [
          (CASTLE, [NNW, N, NNE]),
          (ROAD, [W, E]),
          (FARM, [WNW, ENE]),
          (FARM, [WSW, SSW, S, SSE, ESE]),
          (None, [C])
          ]
      t = tile.Tile('start', clusters)

      self.assertEqual(len(t.sections), 13)

      self.assertEqual(t.sections[N].get_type(), 'C')
      self.assertEqual(t.sections[E].get_type(), 'R')
      self.assertEqual(t.sections[S].get_type(), 'F')
      self.assertEqual(t.sections[W].get_type(), 'R')

      territories = t.get_territories()
      self.assertEqual(len(territories), 4)


  def test_rotate(self):
      clusters = [
          (CASTLE, [NNW, N, NNE]),
          (ROAD, [W, E]),
          (FARM, [WNW, ENE]),
          (FARM, [WSW, SSW, S, SSE, ESE]),
          (None, [C])
          ]
      t = tile.Tile('start', clusters)

      t.rotate()

      self.assertEqual(t.sections[N].get_type(), 'R')
      self.assertEqual(t.sections[E].get_type(), 'C')
      self.assertEqual(t.sections[S].get_type(), 'R')
      self.assertEqual(t.sections[W].get_type(), 'F')
      
      self.assertEqual(t.sections[NNW].get_type(), 'F')
      self.assertEqual(t.sections[WSW].get_type(), 'F')


if __name__ == '__main__':
    unittest.main()
