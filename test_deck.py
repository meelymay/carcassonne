import unittest
import deck

class DeckTest(unittest.TestCase):

  def test_init(self):
      d = deck.Deck()
      for t in d.pile:
          self.assertEqual(len(t.sections), 13)


if __name__ == '__main__':
    unittest.main()
