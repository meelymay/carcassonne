import unittest
import deck
import tile

class TileTest(unittest.TestCase):

  def test_init(self):
      t = tile.Tile('meow', [])
      self.assertEqual(t.name, 'meow')

  def test_connect_model(self):
      secs = [(deck.farm, [deck.top]), (deck.castle, [deck.right]), (deck.road, [deck.left])]
      t = tile.Tile('meow', secs)

      print t.secs[deck.top]

if __name__ == '__main__':
    unittest.main()
