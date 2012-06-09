import httplib, sys
from protocol import *
import time

class CarcassonneClient:
    
    def __init__(self, name):
        self.name = name
        #self.conn = httplib.HTTPConnection('yeast.csail.mit.edu:2222')
        self.conn = httplib.HTTPConnection('localhost:2222')
        header = {}
        header['content-type'] = "join"

        # join the game
        self.conn.request("POST", '/', self.name, header)
        ack = self.conn.getresponse().read()
        if ack in errors:
            print ack
            sys.exit()

        # print 'board',board
        # # show the board
        # SerialGrid.create_grid(board).print_grid()

    def get_board(self):
        header = {}
        header['content-type'] = "board"
        # request the board
        self.conn.request("POST", '/', 'dummy', header)
        board = self.conn.getresponse().read()
        if board in errors:
            print board
            return None
        return SerialGrid.create_grid(board)

    def take_turn(self, wait_time=1):
        # poll server every second
        # until my turn again
        cur_state = self.get_board()
        prev_state = cur_state
        while cur_state is None or \
                prev_state is None or \
                cur_state.player != self.name:
            # show the board if something changed
            if cur_state is not None and prev_state is not None and \
                    cur_state.serialize() != prev_state.serialize():
                cur_state.print_grid()
            # update the prev/cur_state
            time.sleep(wait_time)
            prev_state = cur_state
            cur_state = self.get_board()
        cur_state.print_grid()

        # start turn
        self.start_turn()

        # rotate and place the tile
        placed = False
        while not placed:
            # rotate the tile
            self.rotate()
            # place the tile on the board
            placed = self.place()
            
        # add a meeple
        done_meepling = False
        while not done_meepling:
            done_meepling = self.add_meeple()

        # end turn
        self.end_turn()

    def end_turn(self):
        header = {}
        header['content-type'] = "end_turn"
        
        self.conn.request("POST",'/',self.name,header)
        response = self.conn.getresponse().read()
        if response in errors:
            print response

    def start_turn(self):
        header = {}
        header['content-type'] = "start_turn"
        
        while True:
            self.conn.request("POST",'/',self.name,header)
            response = self.conn.getresponse().read()
            
            if response in errors:
                print response
                time.sleep(1)
            else:
                st = StartTurn.create_turn(response)
                break

        cprint('\n'+self.name+"'s turn",st.color)
        print '\tmeeples:',st.meeples,
        print '\tscore:',st.score
        print 'You have drawn:'
        st.print_tile()

    def rotate(self):
        try:
            i = raw_input('How many clockwise rotations would you like to do? ')
            if len(i) == 0:
                # don't rotate
                rotations = 0
                return
            else:
                rotations = int(i)
        except:
            if i == 'EXIT':
                sys.exit()        
            print 'That is not a valid number of rotations.'
            return

        header = {}
        header['content-type'] = "rotate"
        self.conn.request("POST",'/',json.dumps(rotations),header)
        response = self.conn.getresponse().read()
        
        if response in errors:
            print response
        else:
            SerialGrid.create_grid(response).print_grid()

    def place(self):
        try:
            coord_string = raw_input('Where would you like to place the tile? ')
            if len(coord_string) == 0:
                return False
            coord = tuple([int(i) for i in coord_string.split()])
            if len(coord) != 2:
                print 'That is not a valid coordinate.'
                return False
        except:
            if coord_string == 'EXIT':
                print 'Thanks for playing Carcassonne!'
                sys.exit()
            print 'That is not a valid coordinate.'
            return False

        # try adding to board
        position = json.dumps(coord)
        header = {}
        header['content-type'] = "place"
        self.conn.request("POST",'/',position,header)
        response = self.conn.getresponse().read()

        if response in errors:
            print response
            return False
        else:
            SerialGrid.create_grid(response).print_grid()
            return True

    def add_meeple(self):
        try:
            coord_string = raw_input('Which section of your tile would you like to place the meeple? ')
            if len(coord_string) == 0 or \
                    coord_string.lower().strip() == 'none':
                print 'Not placing a meeple.'
                return True
            
            position = tuple([int(i) for i in coord_string.split()])
            if len(position) != 2:
                print 'That is not a valid section for the meeple.'
                return False
        except:
            if coord_string == 'EXIT':
                print 'Thanks for playing Carcassonne!'
                sys.exit()
            print 'That is not a valid section for the meeple.'
            return False

        header = {}
        header['content-type'] = "meeple"
        self.conn.request("POST",'/',json.dumps(position),header)
        response = self.conn.getresponse().read()
        
        if response in errors:
            print response
            return 'no more meeples' in response
        else:
            SerialGrid.create_grid(response).print_grid()
            return True

if __name__ == '__main__':
    name = sys.argv[1]
    # server = sys.argv[2]
    client = CarcassonneClient(name)
    turn = 0
    while True:
        if turn == 0:
            client.take_turn(wait_time = 3)
        else:
            client.take_turn()
        turn += 1
    
