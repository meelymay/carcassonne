from player import *
from coordinate import *
from section import *


TER_KEY = 'ter key'
N_TILES_KEY = '# tiles key'
N_OPEN_KEY = '# open key'
OWN_KEY = 'own   key'
OLD_OPEN_KEY = 'old open key'
TILE_KEY = 'tile key'


class TerritoryValue:
    def __init__(self, territory, mate=None, meepled=False):
        self.t = territory
        self.score = self.t.calc_score()
        self.owner = self.t.winner()
        self.type = self.t.name
        self.new_territory = meepled

    def fitness(self, heuristics):
        fit = 0

        fit += heristics['score'] * self.score
        fit += heristics[] * self.score

        return heuristics[self.type] * fit

class Play:
    def __init__(self, rotations, coordinate, section):
        self.rotations = rotations
        self.coordinate = coordinate
        self.section = section

    def __hash__(self):
        return self.rotations.__hash__() + self.coordinate.__hash__() + self.section.__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return 'rots: %s\tcoord: %s\tsec:%s' % (self.rotations, self.coordinate, self.section)


class AIPlayer(Player):
    def __init__(self, name, board, params):
        self.board = board
        self.heuristics = params
        Player.__init__(self, name)

    def is_mine(territory, rev=False):
        meeple = territory.get_meeples()
        if meeple:
            mine = meeple[0].name == self.name
            # return true if mine and not rev or not mine and rev
            return mine != rev
        return False

    def has_mine(self, neighbor, rev=False):
        tile, side = neighbor
        t = tile.sections[OPPOSING_DIRECTION[side]].territory
        self.is_mine(t, rev=rev)

    def has_not_mine(self, neighbor):
        return self.has_mine(neighbor, rev=True)

    def territory_value(self, t, mate=None):
        tv = {}
        tv[TER_KEY] = t
        tv[N_TILES_KEY] = len(t.tiles())
        tv[OWN_KEY] = t.winner()

        # calculate how many open sections there are/were
        open_per_sec = 3 if t.name == 'C' else 1
        opens = [x for x in t.sections_open if t.sections_open[x]]
        mate_no = 2
        if mate:
            mate_opens = [x for x in mate.sections_open if mate.sections_open[x]]
            mate_no = len(mate_opens)/open_per_sec
        tv[OLD_OPEN_KEY] = len(opens)/open_per_sec
        tv[N_OPEN_KEY] = tv[OLD_OPEN_KEY] + mate_no - 2
        # missing tiles for cloisters (L)
        if tv[TER_KEY].name == 'L':
            tv[N_OPEN_KEY] = 9-len(t.tiles())

        return tv

    def section_territory(self, sec, neighbors):
        if sec != section.C:
            tile = filter(
                lambda x: sec in section.FULL_SIDE[x[1]],
                neighbors)
            if tile:
                t = tile[0][0].sections[section.OPPOSING_DIRECTION[sec]].territory
                return t
        return None

    def get_fit2(self, coordinate, meeple_sec):
        neighbors = self.board.get_neighbors(coordinate)

        territories = {}

        meeple_territory = self.tile.sections[meeple_sec].territory
        territories[meeple_territory] = TerritoryValue(meeple_territory)

        for sec in self.tile.sections:
            mate = self.tile.sections[sec].territory
            t = self.section_territory(sec, neighbors)
            tv = TerritoryValue(t, mate=mate, meepled=mate == meeple_territory)
            territories[t] = tv

        fit = 0
        for t in territories:
            fit += territories[t].fitness(self.heuristics)

        return fit

    def get_fit(self, coordinate, meeple_sec):
        neighbors = self.board.get_neighbors(coordinate)
        fit = 0
        # len(neighbors)

        nts = {}
        if meeple_sec:
            nt = self.tile.sections[meeple_sec].territory
            ntv = self.territory_value(nt)
            nts[nt] = ntv
            meeple_territory = self.tile.sections[meeple_sec].territory.sections_open
            for sec_obj in meeple_territory:
                msec = [s for s in self.tile.sections if self.tile.sections[s] == sec_obj][0]
                nt = self.section_territory(msec, neighbors)
                if nt and nt not in nts:
                    ntv = self.territory_value(nt, self.tile.sections[msec].territory)
                    # if a territory is already owned, we get no new territory
                    if ntv[OWN_KEY] is not None:
                        print ntv[OWN_KEY], 'already owns'
                        nts = {}
                        break
                    nts[nt] = ntv

        print '\tNEW TER', [str(t) for t in nts]

        ots = {}
        for sec in section.ALL_SIDES:
            if sec == meeple_sec:
                continue
            ot = self.section_territory(sec, neighbors)
            if ot is None or ot in ots:
                continue
            otv = self.territory_value(ot, self.tile.sections[sec].territory)
            ots[ot] = otv

        print '\tOther TER', [str(t) + ' ' + str(ots[t][OWN_KEY]) for t in ots]

        for t in ots:
            if ots[t][OWN_KEY] is None:
                continue
            print '\nOTHER', t.name
            for k in ots[t]:
                print '\t %s:\t%s' % (k, ots[t][k])

        nt_score = 0
        if nts:
            for nt in nts:
                ntv = nts[nt]
                mult = (1 + 1/(ntv[N_OPEN_KEY] + 1)) if nt.name == 'C' else 1
                nt_score = mult*ntv[N_TILES_KEY]
                if nt.name == 'F':
                    nt_score = -100

        mt_score = 0
        for mt in [x for x in ots if ots[x][OWN_KEY] == self.name]:
            mtv = ots[mt]
            mult = 2 if mt.name == 'C' else 1
            if mtv[N_OPEN_KEY] == 0:
                mt_score += mult*mtv[N_TILES_KEY]
            elif mtv[N_OPEN_KEY] < mtv[OLD_OPEN_KEY]:
                mt_score += mult*mtv[N_TILES_KEY]/2
            else:
                mt_score += (1 + 1/(mtv[N_OPEN_KEY] + 1)) if mt.name == 'C' else 1

        ot_score = 0
        for ot in [x for x in ots if ots[x][OWN_KEY] and ots[x][OWN_KEY] != self.name]:
            otv = ots[ot]
            mult = 2 if ot.name == 'C' else 1
            if otv[N_OPEN_KEY] == 0:
                ot_score += mult*otv[N_TILES_KEY]
            elif otv[N_OPEN_KEY] < otv[OLD_OPEN_KEY]:
                ot_score += mult*otv[N_TILES_KEY]/2
            else:
                ot_score += (1 + 1/(otv[N_OPEN_KEY] + 1)) if ot.name == 'C' else 1

        if nt_score+mt_score+ot_score == 0:
            return 0

        # print '\n\n------------------\nFITFITFIT\n---------------------'
        # self.tile.display()
        # print coordinate, meeple_sec
        print '\t\tnew ter score %s,\t my ter score %s,\t opp ter score %s\n' % (nt_score, mt_score, ot_score)
        # for nt in nts:
        #     print '\nNEW TERRITORY', nt.name
        #     for k in nts[nt]:
        #         print '\t%s\t%s' % (k, nts[nt][k])

        fit += (5*nt_score + 2*mt_score - ot_score)*10

        """
        add to an existing castle
                with X tiles
            finish a castle
            add X openings to a castle
            close an opening to a castle
        start a road
            with an end
            with X tiles
        start a cloister
            with X current tiles
            with Y tiles existing for remaining spaces
        FARMING TODO
        STEALING TODO

        features:
            NT = new territory
            NT # tiles
            NT # openings
            NT risk never closing TODO
            NT type

            MT(s) = my territory (already)
            NT # tiles
            NT # openings
            NT risk never closing
            MT type

            OT(s) = oponent territory
            OT # tiles
            OT # openings
            OT risk never closing
            OT type

            TODO empty neighbors
            AR = empty neighbors
            AR # tiles left
            AR # my meeples attached
            AR # opponent meeples attached
        """

        # TODO find neighbors with my territory
        # for neighbor in neighbors:
        #     if section in section.FULL_SIDE[neighbor[1]]
        #     if self.is_mine(neighbor):
        #         fit += 10
        #         break
        #     if self.is_not_mine(neighbor):
        #         fit -= 9
        #         break

        # TODO consider how many potential tiles there are left that could fill that spot

        return fit

    def set_tile(self, tile):
        self.tile = tile.copy()
        board = self.board

        found = False
        possibilities = {}
        for rotation in range(4):
            if found:
                break
            self.rotations = rotation
            if rotation:
                self.tile.rotate()
            print '\nExploring placements for:'
            self.tile.display()
            min_x, max_x, min_y, max_y = board.get_bounds()
            for x in range(min_x-1, max_x+2):
                if found:
                    break
                for y in range(min_y-1, max_y+2):
                    c = Coordinate(x, y)
                    if board.can_place(self.tile, c):
                        print 'Trying Coordinate', c
                        # TODO iter through all sections (just for debug)
                        for sec in [section.N, section.S, section.E, section.W, '']:
                            print '...with meeple', sec
                        # section.ALL_SECTIONS + ['']:
                            p = Play(rotation, c, sec)
                            possibilities[p] = self.get_fit(c, sec)
                            print '\tplay %s fit = %s' % (p, possibilities[p])
                        # found = True
                        # break

        play = max(possibilities, key=lambda x: possibilities[x])
        print 'SELECTED play', play, 'with score', possibilities[play]
        self.rotations = play.rotations
        self.coordinate = play.coordinate
        self.meeple_section = play.section

        # self.meeple_section = ''
        # self.tile = tile.copy()
        # self.tile.rotate_n(self.rotations)
        # secs = self.tile.sections
        # for sec in secs:
        #     t = secs[sec].territory
        #     if t.name == 'C' and not self.is_mine(t):
        #         self.meeple_section = sec
        #         return
        # for sec in secs:
        #     t = secs[sec].territory
        #     if t.name == 'R' and not self.is_mine(t):
        #         self.meeple_section = sec
        #         return

    def get_rotations(self):
        return self.rotations

    def get_coordinate(self):
        return self.coordinate

    def get_meeple_section(self):
        return self.meeple_section
