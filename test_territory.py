import unittest
import territory
from section import *
from tile import *
import deck


class TerritoryTest(unittest.TestCase):

    def test_init(self):
        sections = [Section(None), Section(None), Section(None)]
        t = territory.Territory(sections)

        self.assertEqual(t.is_complete(), False)
        self.assertEqual(len(t.sections_open), 3)

    def test_combine(self):
        s1 = Section(None)
        sections = [s1, Section(None), Section(None)]
        s2 = Section(None)
        sections2 = [s2, Section(None), Section(None), Section(None)]
        t = territory.Territory(sections)
        t2 = territory.Territory(sections2)
        t.combine(s1, t2, s2)

        self.assertEqual(t.is_complete(), False)
        self.assertEqual(len(t.sections_open), 7)

    def test_complete(self):
        s1 = Section(None)
        sections = [s1]
        s2 = Section(None)
        sections2 = [s2]
        t = territory.Territory(sections)
        t2 = territory.Territory(sections2)
        t.combine(s1, t2, s2)

        self.assertEqual(t.is_complete(), True)
        self.assertEqual(len(t.sections_open), 2)

if __name__ == '__main__':
    unittest.main()
