left = (-1,0)
right = (1,0)
top = (0,1)
bottom = (0,-1)

tleft = (-1,1)
tright = (1,1)
bleft = (-1,-1)
bright = (1,-1)

center = (0,0)

# ordered
sides = [left, top, right, bottom]

hor_sides = [left, right]
corners = [tleft, tright, bleft, bright]

full_side = {}
full_side[top] = [tright, top, tleft]
full_side[bottom] = [bright, bottom, bleft]
full_side[right] = [tright, right, bright]
full_side[left] = [bleft, left, tleft]

all_out_secs = [left, tleft, top, tright, right, bright, bottom, bleft]
all_secs = all_out_secs+[center]

rotated_secs = {center:center, left:top, tleft:tright, top:right, tright:bright, right:bottom, bright:bleft, bottom:left, bleft:tleft}

neighbor_secs = {center:[left,top,right,bottom], left:[bleft,tleft], tleft:[left,top], top:[tleft,tright], tright:[top,right], right:[tright,bright], bright:[right,bottom], bottom:[bright,bleft], bleft:[bottom,left]} 

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

        t = Tile('dummy', [(farm,[center]), (farm, all_out_secs)])
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
