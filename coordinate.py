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

class Grid:
    grid = None
    def __init__(self, my_grid):
        Grid.grid = my_grid

def opp_pos(position, horizontal):
    if horizontal:
        return (-1*position[0], position[1])
    else:
        return (position[0], -1*position[1])

    #return tuple([-1*i for i in position])

class Coordinate:
    c1 = 1000
    c2 = 333

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.val = Coordinate.c1*(x+Coordinate.c2) + (y+Coordinate.c2)

    def displayable(self):
        return '('+str(self.x)+','+str(self.y)+')'

    def coord_from_val(val):
        return Coordinate(val/Coordinate.c1-Coordinate.c2, 
                          val%Coordinate.c1-Coordinate.c2)

    def neighbor(self, pos):
        return Coordinate(self.x+pos[0], self.y+pos[1])

