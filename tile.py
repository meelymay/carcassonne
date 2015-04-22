from section import *
from territory import *

ALL_SIDES = []

def opposing_section(section):
    # TODO
    pass

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
        # TODO
        self.name = name
        self.inits = territories
        self.sections = {}

        for territory_type, directions in territories:
            for dir in directions:
                if dir in self.sections:
                    print 'TERRITORIES ', territories
                    print 'SECTIONS ', self.sections
                    raise Exception('Multiple sections for direction: ' + dir)
                self.sections[dir] = Section(self)

            if territory_type:
                create_territory = TERRITORY_TYPES[territory_type]
                territory = create_territory([self.sections[dir] for dir in directions])
            else:
                territory = None

            for dir in directions:
                self.sections[dir].territory = territory

        if len(self.sections) != 13:
            print 'TERRITORIES ', territories
            print 'SECTIONS ', self.sections
            raise Exception('All sections not set.')

    def copy(self):
        return Tile(self.name, self.inits)

    def combine_territories(self, neighbor, side):
        for dir in side:
            section = self.sections[dir]
            neighbor_section = neighbor.sections[OPPOSING_DIRECTION[dir]]
            section.combine(neighbor_section)
    
    def display(self):
#         print [' ' + str(self.sections[N]) + ' ',
#         print str(self.sections[W]) + ' ' + str(self.sections[E]),
#         print ' ' + str(self.sections[S]) + ' ']
        for i in self.displayable():
            print i

    def displayable(self):
        #   [[' ', self.sections[N], ' '],
        #    [self.sections[W], ' ', self.sections[E]],
        #    [' ', self.sections[S], ' ']]

        return ['  ' + str(self.sections[N]) + '  ',
                str(self.sections[W]) + ' ' + str(self.sections[C]) + ' ' +  str(self.sections[E]),
                '  ' + str(self.sections[S]) + '  ']


    def rotate_n(self, rotations):
        for i in range(rotations):
            self.rotate()

    def rotate(self):
        # TODO
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
        self.sections[section].place_meeple(meeple)

    def score(self):
        for territory in self.get_territories():
            territory.score()

    def get_territories(self):
        return set([sec.territory for sec in self.sections.values() if sec.territory != None])
