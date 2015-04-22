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

    def __hash__(self):
        return Coordinate.c1*(self.x+Coordinate.c2) + (self.y+Coordinate.c2)

    def displayable(self):
        return '('+str(self.x)+','+str(self.y)+')'

    def coord_from_val(val):
        return Coordinate(val/Coordinate.c1-Coordinate.c2, 
                          val%Coordinate.c1-Coordinate.c2)

    def neighbor(self, pos):
        return Coordinate(self.x+pos[0], self.y+pos[1])

