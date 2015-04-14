farm = ' '
road = '-'
castle = 'o'
cloister = '^'
road_meeple = '+'
farm_meeple = '*'
castle_meeple = '%'
cloister_meeple = '4'

meepled = {}
meepled[farm] = farm_meeple
meepled[castle] = castle_meeple
meepled[road] = road_meeple
meepled[cloister] = cloister_meeple

model_name = {}
model_name[castle] = 'castle'
model_name[farm] = 'farm'
model_name[road] = 'road'
model_name[cloister] = 'cloister'

marker_color = {}
marker_color[castle] = 'on_red'
marker_color[farm] = 'on_green'
marker_color[road] = 'on_white'
marker_color[cloister] = 'on_green'

def create_model(section):
    if section.marker == castle:
        return Castle(section)
    if section.marker == road:
        return Road(section)
    if section.marker == farm:
        return Farm(section)
    if section.marker == cloister:
        return Cloister(section)

# def print_models():
#     # print 'ALL CURRENT MODELS'
#     # for model in all_models:
#     #     model.print_model()
#     castles = [m for m in all_models if iter(m.secs).next().marker == castle]
#     print 'castles:',len(castles)
#     for c in castles:
#         c.print_model()

#     roads = [m for m in all_models if iter(m.secs).next().marker == road]
#     print 'roads:',len(roads)
#     # for r in roads:
#     #     r.print_model()
#     print 'farms:',len([m for m in all_models if iter(m.secs).next().marker == farm])

class Model:
    
    def __init__(self, section):
        self.secs = set([section])

    def has_meeples(self):
        for sec in self.secs:
            if sec.has_meeple():
                return True
        return False

    # def activate(self):
    #     all_models.add(self)

    def combine(self, other):
        other.secs = other.secs.union(self.secs)
        # update tile references
        for sec in other.secs:
            sec.model = other
        # remove dead ref
        # if self in all_models:
        #     all_models.remove(self)

        # return combined model
        return other

    # TODO don't double count meeples
    def return_meeples(self):
        score = self.complete_score()
        if score > 0:
            for sec in self.secs:
                sec.remove_meeple(score)

    def score_meeples(self):
        score = self.score()
        for sec in self.secs:
            sec.remove_meeple(score)

    def complete_score(self):
        return 0

    def score(self):
        return 0

    def print_model(self):
        print self
        for sec in self.secs:
            sec.print_section()
    
class Castle(Model):
    
    def __init__(self, section):
        Model.__init__(self, section)
        self.openings = set([section])

    def print_openings(self):
        for o in self.openings:
            o.print_section()

    def combine(self, other):
        other.openings = other.openings.union(self.openings)

        other_tiles = set([s.tile for s in other.secs])
        self_tiles = set([s.tile for s in self.secs])
        if (len(self_tiles) == 1 and len(other_tiles) == 1 and \
                iter(self_tiles).next() == iter(other_tiles).next()):
            # we're combining for the same tile, no openings closed
            return Model.combine(self, other)
        # check for closed openings
        openings = list(other.openings)
        for opening in openings:
            all_matched = True
            matches = opening.get_matches()
            # check if all sides of this opening are matched
            for match in matches:
                matched = False
                for o in openings:
                    # we found a match for this side
                    if o.matches(match):
                        matched = True
                        break
                # we didn't find a match for this side
                if not matched:
                    all_matched = False
                    break
            # we found all matches for this opening
            if all_matched:
                other.openings.remove(opening)

        return Model.combine(self, other)

    def complete_score(self):
        if len(self.openings) == 0:
            return len(set([s.tile for s in self.secs]))*2
        return 0

    def score(self):
        return len(set([s.tile for s in self.secs]))

    def displayable(self):
        return 'C'

    def print_model(self):
        Model.print_model(self)
        if len(self.openings) > 0:
            print '\topenings:',len(self.openings)
            for opening in self.openings:
                opening.print_section()

class Road(Model):
    
    def __init__(self, section):
        Model.__init__(self, section)
        self.start = section
        self.end = section

    def length(self):
        return len(set([s.tile for s in self.secs]))

    def ends(self):
        return [s for s in self.secs if s.end]

    def displayable(self):
        return 'R'

    def complete_score(self):
        if len(self.ends()) == 2:
            return self.score()
        return 0

    def score(self):
        return self.length()

    def print_model(self):
        Model.print_model(self)
        print '\tlength:',self.length()
        print '\tends:'
        for e in self.ends():
            print '\t',
            e.print_section()

class Farm(Model):
    
    def __init__(self, section):
        Model.__init__(self, section)
        self.random = None

    def combine(self, other):
        self.random = other.random
        return Model.combine(self, other)

    def score(self):
        castles = set([])
        for sec in self.secs:
            for nb_pos in neighbor_secs[sec.position]:
                nb_sec = sec.tile.secs[nb_pos]
                if nb_sec.marker == castle and nb_sec.model.complete_score() > 0:
                    castles.add(sec.model)
        return len(castles)*3

    def displayable(self):
        return 'F'

class Cloister(Model):
    
    def __init__(self, section):
        Model.__init__(self, section)
        self.more_random = None

    def combine(self, other):
        self.more_random = other.more_random
        return Model.combine(self, other)

    def displayable(self):
        return 'L'
