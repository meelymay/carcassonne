from section import *
from territory import *

ALL_SIDES = []


class Tile:

    def __init__(self, name, territories):
        """
        clusters = [
          (territory, [section1, section2, ...]),
          (castle, [NNW, N, NNE]),
          (road, [W, E]),
          (farm, [WNW, ENE]),
          (farm, [WSW, SSW, S, SSE, ESE]),
          (None, [C])
        ]
        """
        self.name = name
        self.inits = territories
        self.sections = {}

        for territory_type, directions in territories:
            for direc in directions:
                if direc in self.sections:
                    print 'TERRITORIES ', territories
                    print 'SECTIONS ', self.sections
                    raise Exception('Multiple sections for direction: ' + direc)
                self.sections[direc] = Section(self)

            create_territory = TERRITORY_TYPES[territory_type]
            territory = create_territory([self.sections[direc] for direc in directions])

            for direc in directions:
                self.sections[direc].territory = territory

        # close center section
        center = self.sections[C]
        center.territory.close(center)

        if len(self.sections) != 13:
            print 'TERRITORIES ', territories
            print 'SECTIONS ', self.sections
            raise Exception('All sections not set.')

    def copy(self):
        return Tile(self.name, self.inits)

    def can_combine(self, neighbor, side):
        for dir in side:
            section = self.sections[dir]
            neighbor_section = neighbor.sections[OPPOSING_DIRECTION[dir]]
            if not section.can_combine(neighbor_section):
                return False
        return True

    def combine_territories(self, neighbor, side):
        """
        Combine the territories of self and the neighbor to the SIDE side
        """
        for direct in FULL_SIDE[side]:
            opp = OPPOSING_DIRECTION[direct]
            # print 'Combining %s(%s) \tand %s(%s)' % (direct, self.sections[direct].addr(),
            #                                         opp, neighbor.sections[opp].addr())

            section = self.sections[direct]
            neighbor_section = neighbor.sections[OPPOSING_DIRECTION[direct]]
            section.combine(neighbor_section)

        center = self.sections[C]
        neighbor_center = neighbor.sections[C]
        if center.territory.name == 'L':
            center.combine(neighbor_center, cloister=True)
        if neighbor_center.territory.name == 'L':
            neighbor_center.combine(center, cloister=True)

    def display(self):
        for i in self.displayable():
            print i

    def displayable(self):
        return map(lambda sec_list: ''.join(map(lambda sec: str(self.sections[sec]), sec_list)),
                   [[WNW, NNW, N, NNE, ENE],
                    [W, W, C, E, E],
                    [WSW, SSW, S, SSE, ESE]])

    def rotate_n(self, rotations):
        for i in range(rotations):
            self.rotate()

    def rotate(self):
        new_sections = {}

        new_sections[C] = self.sections[C]

        new_sections[NNW] = self.sections[WSW]
        new_sections[N] = self.sections[W]
        new_sections[NNE] = self.sections[WNW]

        new_sections[ENE] = self.sections[NNW]
        new_sections[E] = self.sections[N]
        new_sections[ESE] = self.sections[NNE]

        new_sections[SSE] = self.sections[ENE]
        new_sections[S] = self.sections[E]
        new_sections[SSW] = self.sections[ESE]

        new_sections[WSW] = self.sections[SSE]
        new_sections[W] = self.sections[S]
        new_sections[WNW] = self.sections[SSW]

        self.sections = new_sections

    def place_meeple(self, section, meeple):
        return self.sections[section].place_meeple(meeple)

    def score(self, end_game=False):
        for territory in self.get_territories():
            territory.score(end_game)

    def display_addrs(self):
        def pretty(x):
            sec = self.sections[x]
            ter = sec.territory
            return sec.addr() + ':' + ter.name + str(ter.id)

        print '%s\t%s\t%s\t%s\t%s' % tuple([pretty(x) for x in [WNW, NNW, N, NNE, ENE]])
        print '%s\t%s\t%s\t%s\t%s' % tuple([pretty(x) for x in [W, W, C, E, E]])
        print '%s\t%s\t%s\t%s\t%s' % tuple([pretty(x) for x in [WSW, SSW, S, SSE, ESE]])

    def get_territories(self):
        return set([sec.territory for sec in self.sections.values() if sec.territory is not None])
