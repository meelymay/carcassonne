import random

FARM = 'farm'
CASTLE = 'castle'
ROAD = 'road'
CLOISTER = 'cloister'


class Territory:

    def __init__(self, sections):
        self.sections_open = dict([(sec, True) for sec in sections])
        self.id = int(random.random()*1000)
        self.name = 'EMPTY'

    def close(self, section):
        self.sections_open[section] = False

    def combine(self, section, neighbor, neighbor_sec):
        if self.name != neighbor.name:
            raise Exception('Adjacent sections must be the same!')
        # if the neighbor is not already part of the territory
        if self != neighbor:
            # for all of the sections in the neighbor
            for sec in neighbor.sections_open:
                # set the territory of the section to this one
                sec.territory = self
                # if the section hasn't already been added to this territory,
                if sec not in self.sections_open:
                    # add it to this territories sections
                    self.sections_open[sec] = neighbor.sections_open[sec]

        # close the two sections that were neighboring each other
        self.sections_open[section] = False
        self.sections_open[neighbor_sec] = False

    def tiles(self):
        return set([sec.tile for sec in self.sections_open])

    def is_complete(self):
        opens = self.sections_open
        return True not in opens.values()

    def score(self):
        if self.is_complete():
            s = len(self.tiles())
            self.replace_meeples(s)
            return s
        else:
            return 0

    def get_meeples(self):
        return [sec.meeple for sec in self.sections_open if sec.meeple is not None]

    def replace_meeples(self, s):
        # TODO find out who wins territory?
        color = 'dan'
        for sec in self.sections_open:
            meeple = sec.meeple
            sec.meeple = None
            if not meeple:
                continue
            if color == meeple.color:
                meeple.replace(s)
            else:
                meeple.replace(0)

    def display(self):
        for tile in self.tiles():
            tile.display()
            for section in tile.sections.values():
                if section in self.sections_open:
                    print section, self.sections_open[section]

    def __str__(self):
        s = ''
        s += '%s ter%s = ' % (self.name, self.id)
        for sec in self.sections_open:
            if self.sections_open[sec]:
                s += '\t%s,' % sec.addr()

        return s


class Castle(Territory):
    def __init__(self, sections):
        Territory.__init__(self, sections)
        self.name = 'C'


class Road(Territory):
    def __init__(self, sections):
        Territory.__init__(self, sections)
        self.name = 'R'


class Farm(Territory):
    def __init__(self, sections):
        Territory.__init__(self, sections)
        self.name = 'F'


class Cloister(Territory):
    def __init__(self, sections):
        Territory.__init__(self, sections)
        self.name = 'L'

    def is_complete(self):
        return False


TERRITORY_TYPES = {
    FARM: Farm,
    CASTLE: Castle,
    CLOISTER: Cloister,
    ROAD: Road
}
