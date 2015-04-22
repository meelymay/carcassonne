FARM = 'farm'
CASTLE = 'castle'
ROAD = 'road'
CLOISTER = 'cloister'

class Territory:

    def __init__(self, sections):
        self.sections_open = dict([(sec, True) for sec in sections])

    def combine(self, section, neighbor, neighbor_sec):
        if self.name != neighbor.name:
            raise Exception('Adjacent sections must be the same!')
        if self != neighbor:
            for sec in neighbor.sections_open:
                self.sections_open[sec] = neighbor.sections_open[sec]

        self.sections_open[section] = False
        self.sections_open[neighbor_sec] = False

    def tiles(self):
        return set([sec.tile for sec in self.sections_open])

    def is_complete(self):
        return True not in self.sections_open.values()

    def score(self):
        if self.is_complete():
            self.replace_meeples()
            return len(self.tiles())
        else:
            return 0

    def replace_meeples(self):
        # TODO
        # find out who wins?
        meeples = [sec.meeple for sec in self.sections_open if sec.meeple != None]

        meeples[0].replace(self.score())

class Castle(Territory):
    def __init__(self, sections):
        self.name = 'C'
        Territory.__init__(self, sections)

class Road(Territory):
    def __init__(self, sections):
        self.name = 'R'
        Territory.__init__(self, sections)

class Farm(Territory):
    def __init__(self, sections):
        self.name = 'F'
        Territory.__init__(self, sections)

class Cloister(Territory):
    def __init__(self, sections):
        self.name = 'L'
        Territory.__init__(self, sections)

TERRITORY_TYPES = {
    FARM: Farm,
    CASTLE: Castle,
    CLOISTER: Cloister,
    ROAD: Road
}

