from coordinate import *
from model import *
import sys

class Section:
    def __init__(self, tile, position, marker, end=False):
        self.tile = tile
        self.position = position
        self.marker = marker
        self.end = end
        self.model = None
        self.meeple = None

    def make_end(self):
        self.end = True

    def set_model(self, model):
        self.model = model

    def add_meeple(self, meeple):
        if self.model.has_meeples():
            return False
        else:
            self.meeple = meeple
            meeple.set_section(self)
            return True

    def remove_meeple(self, score):
        if self.meeple:
            self.meeple.repossess(score)
            self.meeple = None

    def has_meeple(self):
        return self.meeple is not None

    def get_matches(self):
        matches = []

        t = Tile('dummy',farm,farm,farm,farm)
        for horizontal in [True, False]:
            pos = opp_pos(self.position, horizontal)
            if pos != self.position:
                coo = self.tile.coordinate.neighbor(self.position)
                t = t.copy()
                t.activate(coo)
                matches.append(Section(t, pos, self.marker))

        return matches

    def matches(self, other):
        return self.tile.coordinate.val == other.tile.coordinate.val and \
            self.position == other.position

    def connectable(self, other):
        return self.marker == other.marker

    def print_section(self):
        print '\t', self.tile.name, self.tile.coordinate.displayable(), '\t', self.position, '\t', self.marker

    def displayable(self):
        if self.meeple:
            return (meepled[self.marker], 
                    self.meeple.get_color(),
                    marker_color[self.marker])
        else:
            return (self.marker, 
                    None,
                    marker_color[self.marker])

class Tile:

    def __init__(self, name, l, t, r, b, connected=False):
        self.name = name
        self.connected = connected

        self.secs = {}
        # setting top, bottom, left, right
        self.secs[left] = Section(self, left, l)
        self.secs[top] = Section(self, top, t)
        self.secs[right] = Section(self, right, r)
        self.secs[bottom] = Section(self, bottom, b)

        # make roads end
        roads = [self.secs[s] for s in self.secs if self.secs[s].marker == road]
        if len(roads) != 2 and len(roads) > 0:
            map(Section.make_end, roads)

        # setting corners
        for pos in corners:
            self.secs[pos] = Section(self, pos, farm)

        # set center
        self.secs[center] = Section(self, center, farm)
        if self.connected:
            self.secs[center] = Section(self, center, castle)
        if 'cloister' in self.name:
            self.secs[center] = Section(self, center, cloister)
        if len(roads) == 2:
            self.secs[center] = Section(self, center, road)

        # linking to model
        self.model = {}
        for sec in all_secs:
            self.secs[sec].set_model(create_model(self.secs[sec]))
        self.connect_model()

    def connect_model(self):

        # connect casltes
        if self.connected:
            sections = [self.secs[s] for s in sides if self.secs[s].marker == castle]
            self.connect_sections(sections)

        # connect roads
        road_secs = [self.secs[s] for s in sides if self.secs[s].marker == road]
        if len(road_secs) == 2:
            self.connect_sections(road_secs)

        # connect farms
        for side in sides:
            # unify sides
            if self.secs[side].marker == farm:
                farm_side = [self.secs[s] for s in full_side[side]]
                self.connect_sections(farm_side)
        # adjacent sides
        prev_side = sides[-1]
        for side in sides:
            if self.secs[prev_side].marker == farm and \
                    self.secs[side].marker == farm:
                self.connect_sections([self.secs[prev_side], 
                                       self.secs[side]])
            prev_side = side
        # farm_castle2 exception
        if self.name == 'farm_castle2':
            self.connect_sections(
                [self.secs[s] for s in sides if self.secs[s].marker == farm])

    def connect_sections(self, sections):
        mod = None
        for sec in sections:
            if mod:
                sec.model = sec.model.combine(mod)
            else:
                mod = sec.model

    def print_tile(self):
        print self.name
        for sec in self.secs:
            self.secs[sec].print_section()

    def add_meeple(self, position, meeple):
        section = self.secs[position]
        if section.add_meeple(meeple):
            return None
        else:
            print 'That',model_name[section.marker],'already has a meeple.'
            return meeple

    # def return_meeples(self):
    #     for pos in self.secs:
    #         section = self.secs[pos]
    #         if section.model.is_complete():
    #             section.model.return_meeples()

    def activate(self, coordinate):
        self.coordinate = coordinate
        # print self.secs
        for sec in self.secs:
            if sec == (0,0):
                continue
            #self.secs[sec].model.activate()

    def copy(self):
        return Tile(self.name, 
                    self.secs[left].marker, 
                    self.secs[top].marker, 
                    self.secs[right].marker,
                    self.secs[bottom].marker,
                    self.connected)

    def rotate_n(self, n):
        for i in range(n):
            self.rotate()

    def rotate_cc(self):
        self.rotate(3);

    def rotate(self):
        for i in range(6):
            prev_sec = all_out_secs[0]
            tmp = self.secs[prev_sec]
            for sec in all_out_secs[1:]:
                self.secs[prev_sec] = self.secs[sec]
                self.secs[prev_sec].position = prev_sec
                prev_sec = sec
            self.secs[prev_sec] = tmp
            self.secs[prev_sec].position = prev_sec

    def display(self):
        d = self.displayable()
        for i in range(len(d)):
            for j in range(3):
                print d[i][j][0],
            print

    def gridify(self):
        d = self.displayable()
        grid = []
        grid.append([])
        y = 0
        for i in range(len(d)):
            for j in range(3):
                grid[y].append(d[i][j])
                grid[y].append((' ',
                                d[i][j][1],
                                d[i][j][2]))
            grid.append([])
            y += 1
        return grid

    def displayable(self):
        if self.connected:
            center = ' '+castle+' '
        else:
            center = ' . '
        d = []
        for y in [1, 0, -1]:
            di = []
            for x in [-1, 0, 1]:
                pos = (x,y)
                if pos == (0,0):
                    if self.name == 'start_tile':
                        di.append(('X','grey','on_white'))
                    elif self.secs[pos].marker == farm:
                        di.append(('.',None,'on_green'))
                    else:
                        di.append(self.secs[pos].displayable())
                else:
                    di.append(self.secs[pos].displayable())
                
            d.append(di)

        # for i in range(len(d)):
        #     for j in range(3):
        #         print d[i][j][0],
        #     print
        return d

    def display_mods(self):
        print self.name
        for i in [1, 0, -1]:
            for j in [-1, 0, 1]:
                print self.secs[(j, i)].model.displayable(),
            print
        print

    def display_tile(self):
        print 'TILE',self.name,'(',self.coordinate.x,',',self.coordinate.y,')'

def combine_tile_models(new_tile, board_tile, side):
    rel_sides = full_side[side]
    # print rel_sides
    # print new_tile.name
    # new_tile.display()
    # print board_tile.name
    # board_tile.display()

    # combine each section of the relevant side
    for sec in rel_sides:

        board_model = board_tile.secs[opp_pos(sec, side in hor_sides)].model
        new_model = new_tile.secs[sec].model
        # set new_tile's model to board's new combined model
        new_tile.secs[sec].model = new_model.combine(board_model)

        # if new_tile.secs[sec].marker == castle:
            # print 'NEW TILE OPENINGS'
            # new_tile.secs[sec].model.print_openings()

        # except:
        #     new_tile.display_mods()
        #     board_tile.display_mods()

        #     for sec in all_secs:
        #         print sec
        #         print 'new',new_tile, '\t', new_tile.secs[sec].model
        #         print 'board',board_tile, '\t', board_tile.secs[sec].model
        #     sys.exit()
