from termcolor import cprint, colored

def num_3string(i):
    if i >= 0:
        if abs(i) > 10:
            return str(i)+' '
        else:
            return ' '+str(i)+' '
    else:
        if abs(i) > 10:
            return str(i)
        else:
            return str(i)+' '

def num_5string(i):
    if i == ' ':
        return '     '
    if i >= 0:
        if abs(i) >= 10:
            return ' '+str(i)+'  '
        else:
            return '  '+str(i)+'  '
    else:
        if abs(i) >= 10:
            return ' '+str(i)+' '
        else:
            return ' '+str(i)+'  '

def display(board):
    # width of row numbers
    print '    ',
    # column numbers
    for i in range(board.min_x, board.max_x+1):
        print num_5string(i),
    print
    # each row on board
    for y in range(board.max_y, board.min_y-1,-1):
        # row number
        for i in range(3):
            if i == 1:
               print num_5string(y),
            else:
               print num_5string(' '),
            # each column on board
            for x in range(board.min_x, board.max_x+1):
                c = Coordinate(x,y) 
                if c.val in board.grid:
                    tmp_tile = board.grid[c.val]
                    tmp_disp = tmp_tile.displayable()
                    for j in range(3):
                        if tmp_disp[i][j][1] is None:
                            bold = []
                        else:
                            bold = ['bold']
                        cprint(tmp_disp[i][j][0]+' ', 
                               tmp_disp[i][j][1],
                               tmp_disp[i][j][2], 
                               end='',
                               attrs=bold)
                # empty tile
                else:
                    print num_5string(' '),
            print

    def print_models(self):
        models = self.get_model_sections()

        castles = set([m.model for m in models if m.marker == castle])
        farms = set([m.model for m in models if m.marker == farm])
        roads = set([m.model for m in models if m.marker == road])

        print 'CASTLES:',len(castles)
        for model in castles:
            model.print_model()
        print 'ROADS:',len(roads)
        for model in roads:
            model.print_model()
        print 'FARMS:',len(farms)
        for model in farms:
            model.print_model()

    def get_grid(self):
        grid = {}

        # width of row numbers
        grid[0] = []
        print '    ',
        # column numbers
        for i in range(self.min_x, self.max_x+1):
            print num_5string(i),
        print
        # each row on board
        for y in range(self.max_y, self.min_y-1,-1):
            # row number
            for i in range(3):
                if i == 1:
                    print num_5string(y),
                else:
                    print num_5string(' '),
                # each column on board
                for x in range(self.min_x, self.max_x+1):
                    c = Coordinate(x,y) 
                    # other tile
                    if c.val in self.grid:
                        tmp_tile = self.grid[c.val]
                        tmp_disp = tmp_tile.displayable()
                        for j in range(3):
                            if tmp_disp[i][j][1] is None:
                                bold = []
                            else:
                                bold = ['bold']
                            cprint(tmp_disp[i][j][0]+' ', 
                                   tmp_disp[i][j][1],
                                   tmp_disp[i][j][2], 
                                   end='',
                                   attrs=bold)
                    # empty tile
                    else:
                        print num_5string(' '),
                print

