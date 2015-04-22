import unittest
import game

class GameTest(unittest.TestCase):

  def test_init(self):
      g = game.Game(['Amelia', 'Dan'])
      self.assertEqual(g.player.name, 'Amelia')

if __name__ == '__main__':
    unittest.main()
