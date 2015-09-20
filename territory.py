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
                # TODO (bug) sometimes territories are closing early
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

    def calc_score(self, end_game=False):
        return len(self.tiles())

    def score(self, end_game=False):
        if end_game or self.is_complete():
            s = self.calc_score(end_game=end_game)
            self.replace_meeples(s)
            return s
        else:
            return 0

    def get_meeples(self):
        return [sec.meeple for sec in self.sections_open if sec.meeple is not None]

    def replace_meeples(self, s):
        # TODO find out who wins territory?
        player = None
        for sec in self.sections_open:
            meeple = sec.meeple
            sec.meeple = None
            if not meeple:
                continue
            if player is None:
                player = meeple.name
            if player == meeple.name:
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

    def calc_score(self, end_game=False):
        s = len(self.tiles())
        if end_game:
            return s
        else:
            return s*2


class Road(Territory):
    def __init__(self, sections):
        Territory.__init__(self, sections)
        self.name = 'R'


class Farm(Territory):
    def __init__(self, sections):
        Territory.__init__(self, sections)
        self.name = 'F'

    def calc_score(self, end_game=False):
        castles = set()
        tiles = self.tiles()
        for tile in tiles:
            territories = tile.get_territories()
            for neighbor in territories:
                # TODO exclude castles not adjacent to farm
                if neighbor.name == 'C' and neighbor.is_complete():
                    castles.add(neighbor)

        return len(castles)*3

    def is_complete(self):
        return False


class Cloister(Territory):
    def __init__(self, sections):
        Territory.__init__(self, sections)
        self.name = 'L'
        self.center = sections[0]

    def get_meeples(self):
        meeple = self.center.meeple
        if meeple:
            return [meeple]
        else:
            return None

    def combine(self, section, neighbor, neighbor_sec):
        self.sections_open[neighbor_sec] = True

    def is_complete(self):
        return len(self.tiles()) == 9


TERRITORY_TYPES = {
    FARM: Farm,
    CASTLE: Castle,
    CLOISTER: Cloister,
    ROAD: Road
}
