import BaseHTTPServer
import time
from carcassonne import *

#HOST_NAME = 'localhost'
#PORT_NUMBER = 2222

HOST_NAME = 'chili.csail.mit.edu'
PORT_NUMBER = 2222

class CarcassonneServer(BaseHTTPServer.BaseHTTPRequestHandler):

    game = None
    players = []
    tile = None
    game_over = False

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("Don't GET me bro!")

    def do_POST(self):
        if CarcassonneServer.game is not None:
            player = CarcassonneServer.game.player
        else:
            player = None

        text = "Bad request."

        request_types = ['join',
                         'start',
                         'board',
                         'start_turn',
                         'rotate',
                         'place',
                         'meeple',
                         'end_turn']
        content_type = self.headers.getheader('content-type')
        print '\n CONTENT TYPE',content_type,'\n'
        if content_type in request_types:
            length = int(self.headers.getheader('content-length'))
            content = self.rfile.read(length)
        else:
            text = 'Bad request.'
            text = text.encode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(text)
            return

        # print 'headers:',self.headers #.getheader('content-type')
        if content_type == "join":
            # add player to players
            name = content.strip()
            CarcassonneServer.players.append(name)
            print '\nADDING',name,'TO PLAYS.',CarcassonneServer.players,'\n'
            if len(CarcassonneServer.players) == 2:
                # start the game
                CarcassonneServer.game = Game(CarcassonneServer.players)
            
            # ACK
            text = 'added '+name
            text = text.encode('utf-8')
        elif content_type == "start":
            # start the game
            CarcassonneServer.game = Game(CarcassonneServer.players)

            # ACK
            text = 'starting'
            text = text.encode('utf-8')
        elif content_type == "board":
            # respond with the board 
            if CarcassonneServer.game is None:
                text = errors[6] # 'Game has not started yet.'
            else:
                text = SerialGrid(CarcassonneServer.game.board, 
                                  player.name).serialize()
            text = text.encode('utf-8')
        elif content_type == "start_turn":
            # make sure the right player is starting
            # if CarcassonneServer.players[self.client_address] != player.name:
            #     text = errors[3] # 'It is not your turn!'


            CarcassonneServer.tile = CarcassonneServer.game.draw()
            if not CarcassonneServer.tile:
                CarcassonneServer.game_over = True
                text = errors[-1] # 'GAME OVER'
            else:
                # give stats for start of turn
                st = StartTurn(player.color,
                               player.num_meeples(),
                               player.score,
                               CarcassonneServer.tile)
                text = st.serialize()

            text = text.encode('utf-8')
        elif content_type == "rotate":

            # if CarcassonneServer.players[self.client_address] != player.name:
            #     text = errors[3] # 'It is not your turn

            # rotate the tile
            rotations = json.loads(content)
            CarcassonneServer.tile = CarcassonneServer.game.rotate(rotations)

            # respond with rotated tile
            text = json.dumps({'grid': CarcassonneServer.tile,
                               'player': 'dummy'})
            text = text.encode('utf-8')
        elif content_type == "place":
            # get position
            position = json.loads(content)

            # place the tile
            placed = CarcassonneServer.game.place(position)
            if placed:
                text = SerialGrid(CarcassonneServer.game.board, 
                                  player.name).serialize()
            else:
                text = errors[1] # 'You cannot place that tile there.'
            text = text.encode('utf-8')
        elif content_type == "meeple":
            if player.num_meeples() == 0:
                text = errors[2] # 'You have no more meeples.'
            else:
                section = tuple(json.loads(content))
                added = CarcassonneServer.game.add_meeple(section)
                
            if added:
                text = SerialGrid(CarcassonneServer.game.board, 
                                  player.name).serialize()
            else:
                text = errors[3] # 'You cannot place a meeple there.'
            text = text.encode('utf-8')
        elif content_type == "end_turn":
            CarcassonneServer.game.return_meeples()
            CarcassonneServer.game.next_player()

            # ACK
            text = 'cleaned'
            text = text.encode('utf-8')
        else:
            print 'not text/html'

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(text)

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), CarcassonneServer)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
