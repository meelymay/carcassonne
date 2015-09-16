import unittest
import tile
import deck
from territory import *
from section import *


class TileTest(unittest.TestCase):

    def test_init(self):
        clusters = [
            (CASTLE, [NNW, N, NNE]),
            (ROAD, [W, E]),
            (FARM, [WNW, ENE]),
            (FARM, [WSW, SSW, S, SSE, ESE]),
            (FARM, [C])
            ]
        t = tile.Tile('start', clusters)

        self.assertEqual(len(t.sections), 13)

        self.assertEqual(t.sections[N].get_type(), 'C')
        self.assertEqual(t.sections[E].get_type(), 'R')
        self.assertEqual(t.sections[S].get_type(), 'F')
        self.assertEqual(t.sections[W].get_type(), 'R')

        territories = t.get_territories()
        self.assertEqual(len(territories), 5)

    def test_rotate(self):
        clusters = [
            (CASTLE, [NNW, N, NNE]),
            (ROAD, [W, E]),
            (FARM, [WNW, ENE]),
            (FARM, [WSW, SSW, S, SSE, ESE]),
            (FARM, [C])
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
            (FARM, [C])
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
            (FARM, [C])
            ]
        t = tile.Tile('start', clusters)
        n = t.copy()
        n.rotate_n(2)

        t.combine_territories(n, N)

        territory = t.sections[N].territory

        territory.display()

        self.assertEqual(territory.is_complete(), True)

        # castle2
        c1 = deck.CASTLE_END.copy()
        c2 = deck.CASTLE2.copy()
        c3 = deck.CASTLE_END.copy()
        c3.rotate()

        c1.combine_territories(c2, N)
        c2.combine_territories(c3, W)

        t = c1.sections[N].territory
        self.assertTrue(territory.is_complete())

        # castle3
        c1 = deck.CASTLE_END.copy()
        c2 = deck.CASTLE3.copy()
        c3 = deck.CASTLE_END.copy()
        c4 = deck.CASTLE_END.copy()
        c2.rotate_n(2)
        c3.rotate()
        c4.rotate_n(3)

        c1.display()
        c2.display()
        c3.display()
        c4.display()

        c1.combine_territories(c2, N)
        c2.combine_territories(c3, W)
        c2.combine_territories(c4, E)

        t = c1.sections[N].territory
        self.assertTrue(territory.is_complete())

        # castle3_road
        c1 = deck.CASTLE3_ROAD.copy()
        c2 = deck.CASTLE_END.copy()
        c3 = deck.CASTLE_END.copy()
        c4 = deck.CASTLE_END.copy()
        c1.rotate_n(2)
        c3.rotate()
        c4.rotate_n(3)

        c1.display()
        c2.display()
        c3.display()
        c4.display()

        c1.combine_territories(c2, S)
        c1.combine_territories(c3, W)
        c1.combine_territories(c4, E)

        t = c1.sections[N].territory
        self.assertTrue(territory.is_complete())

if __name__ == '__main__':
    unittest.main()
