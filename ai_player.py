from player import *
from coordinate import *
from section import *


TER_KEY = 'ter key'
N_TILE_KEY = 'tile key'
N_OPEN_KEY = 'open key'
OWN_KEY = 'own   key'
OLD_OPEN_KEY = 'old open key'


class Play:
    def __init__(self, rotations, coordinate, section):
        self.rotations = rotations
        self.coordinate = coordinate
        self.section = section

    def __hash__(self):
        return self.rotations.__hash__() + self.coordinate.__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


class AIPlayer(Player):
    def __init__(self, name, board):
        self.board = board
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

    def territory_value(self, t, mate):
        tv = {}
        tv[TER_KEY] = t
        tv[N_TILE_KEY] = len(t.tiles())

        open_per_sec = 3 if t.name == 'C' else 1
        opens = [x for x in t.sections_open if t.sections_open[x]]
        mate_opens = [x for x in mate.sections_open if mate.sections_open[x]]
        mate_no = len(mate_opens)/open_per_sec
        tv[OLD_OPEN_KEY] = len(opens)/open_per_sec
        tv[N_OPEN_KEY] = tv[OLD_OPEN_KEY] + mate_no - 2

        if tv[TER_KEY].name == 'L':
            tv[N_OPEN_KEY] = 9-len(t.tiles())
        tv[OWN_KEY] = t.winner()
        return tv

    def section_territory(self, sec, neighbors):
        if sec != section.C:
            tile = filter(
                lambda x: sec in section.FULL_SIDE[x[1]],
                neighbors)
            if tile:
                t = tile[0][0].sections[section.OPPOSING_DIRECTION[sec]].territory
                if not t.winner():
                    return t
        return None

    def get_fit(self, coordinate, meeple_sec):
        neighbors = self.board.get_neighbors(coordinate)
        fit = len(neighbors)

        nt = self.section_territory(meeple_sec, neighbors)
        if nt:
            ntv = self.territory_value(nt, self.tile.sections[meeple_sec].territory)

        ots = {}
        for sec in section.ALL_SIDES:
            if sec == meeple_sec:
                continue
            ot = self.section_territory(sec, neighbors)
            if ot is None or ot in ots:
                continue
            otv = self.territory_value(ot, self.tile.sections[sec].territory)
            ots[ot] = otv

        # if nt:
        #     print nt
        #     for k in ntv:
        #         print '\t%s\t%s' % (k, ntv[k])

        # for t in ots:
        #     print t, '\t', ots[t][N_TILE_KEY]

        nt_score = 0
        if nt:
            mult = (1 + 1/(ntv[N_OPEN_KEY] + 1)) if nt.name == 'C' else 1
            nt_score = mult*ntv[N_TILE_KEY]

        mt_score = 0
        for mt in [x for x in ots if ots[x][OWN_KEY] == self.name]:
            mtv = ots[mt]
            mult = 2 if mt.name == 'C' else 1
            if mtv[N_OPEN_KEY] == 0:
                mt_score += mult*mtv[N_TILE_KEY]
            elif mtv[N_OPEN_KEY] < mtv[OLD_OPEN_KEY]:
                mt_score += mult*mtv[N_TILE_KEY]/2
            else:
                mt_score += (1 + 1/(mtv[N_OPEN_KEY] + 1)) if mt.name == 'C' else 1

        ot_score = 0
        for ot in [x for x in ots if ots[x][OWN_KEY] and ots[x][OWN_KEY] != self.name]:
            otv = ots[ot]
            mult = 2 if ot.name == 'C' else 1
            if otv[N_OPEN_KEY] == 0:
                ot_score += mult*otv[N_TILE_KEY]
            elif otv[N_OPEN_KEY] < otv[OLD_OPEN_KEY]:
                ot_score += mult*otv[N_TILE_KEY]/2
            else:
                ot_score += (1 + 1/(otv[N_OPEN_KEY] + 1)) if ot.name == 'C' else 1

        # print 'new ter score %s,\t my ter score %s,\t opp ter score %s' % (nt_score, mt_score, ot_score)
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
            min_x, max_x, min_y, max_y = board.get_bounds()
            for x in range(min_x-1, max_x+2):
                if found:
                    break
                for y in range(min_y-1, max_y+2):
                    c = Coordinate(x, y)
                    if board.can_place(self.tile, c):
                        for sec in section.ALL_SECTIONS + ['']:
                            possibilities[Play(rotation, c, sec)] = self.get_fit(c, sec)
                        # found = True
                        # break

        play = max(possibilities, key=lambda x: possibilities[x])
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
