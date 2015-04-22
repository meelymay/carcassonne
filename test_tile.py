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

      self.assertEqual(len(t.sections), 13)

  def test_can_combine(self):
      clusters = [
          (CASTLE, [NNW, N, NNE]),
          (ROAD, [W, E]),
          (FARM, [WNW, ENE]),
          (FARM, [WSW, SSW, S, SSE, ESE]),
          (None, [C])
          ]
      t = tile.Tile('start', clusters)
      n = t.copy()

      self.assertEqual(t.can_combine(n, E), True)
      self.assertEqual(t.can_combine(n, N), False)

      n.rotate_n(2)
      self.assertEqual(t.can_combine(n, N), True)
      self.assertEqual(t.can_combine(n, W), True)

  def test_combine(self):
      clusters = [
          (CASTLE, [NNW, N, NNE]),
          (ROAD, [W, E]),
          (FARM, [WNW, ENE]),
          (FARM, [WSW, SSW, S, SSE, ESE]),
          (None, [C])
          ]
      t = tile.Tile('start', clusters)
      n = t.copy()

      n.rotate_n(2)
      t.combine_territories(n, N)

      territory = list(t.get_territories())[0]

      self.assertEqual(territory.is_complete(), True)


if __name__ == '__main__':
    unittest.main()
