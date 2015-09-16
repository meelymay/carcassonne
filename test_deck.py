import unittest
import deck


class DeckTest(unittest.TestCase):

    def test_init(self):
        d = deck.Deck()
        for t in d.pile:
            self.assertEqual(len(t.sections), 13)

    def test_territories(self):
        self.assertEquals(len(deck.CLOISTER_PLAIN.get_territories()), 2)

        self.assertEquals(len(deck.CLOISTER_ROAD.get_territories()), 3)
        self.assertEquals(len(deck.CASTLE4.get_territories()), 1)
        self.assertEquals(len(deck.CASTLE3.get_territories()), 2)
        self.assertEquals(len(deck.CASTLE3_ROAD.get_territories()), 4)
        self.assertEquals(len(deck.CASTLE2.get_territories()), 2)
        self.assertEquals(len(deck.CASTLE2_ROAD.get_territories()), 4)
        self.assertEquals(len(deck.CASTLE_FARM2.get_territories()), 3)
        self.assertEquals(len(deck.FARM_CASTLE2.get_territories()), 3)
        self.assertEquals(len(deck.BUTT.get_territories()), 3)
        self.assertEquals(len(deck.CASTLE_END.get_territories()), 2)
        self.assertEquals(len(deck.CASTLE_END_ROAD_L.get_territories()), 4)
        self.assertEquals(len(deck.CASTLE_END_ROAD_R.get_territories()), 4)
        self.assertEquals(len(deck.CASTLE_END_ROAD3.get_territories()), 8)
        self.assertEquals(len(deck.CASTLE_END_ROAD.get_territories()), 4)
        self.assertEquals(len(deck.ROAD_TILE.get_territories()), 3)
        self.assertEquals(len(deck.ROAD_BEND.get_territories()), 3)
        self.assertEquals(len(deck.ROAD3.get_territories()), 7)
        self.assertEquals(len(deck.ROAD4.get_territories()), 9)

if __name__ == '__main__':
    unittest.main()
