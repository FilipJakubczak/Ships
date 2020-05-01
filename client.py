import socket
import threading as thread
import json
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12340       # The port used by the server


class Client:
    def __init__(self, host, port):
        self.host, self.port = host, port
        self.sock = None
        self.name = None
        self.game_finished = False
        self.turn = None

    def start(self):
        """Try to join the game and play."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.sock = s
            self.connect()
            self.set_name()
            self.send_msg({'type': 'connect', 'data': self.name})
            listener = thread.Thread(target=self.listener)
            listener.start()
            listener.join()

    def connect(self):
        """Connect to the server."""
        try:
            self.sock.connect((self.host, self.port))
        except Exception as ex:
            print(ex)
            print('Could not connect to server.')
            sys.exit(1)
        print('Connected to server.')

    def set_name(self):
        """Set player nickname."""
        nick = input('Your nickname: ')
        self.name = nick

    def send_msg(self, msg):
        """Send a message to the server."""
        msg = json.dumps(msg)
        self.sock.send(msg.encode('utf-8'))

    def listener(self):
        """A listener that responds to messages from the server."""
        while not self.game_finished:
            try:
                data = self.sock.recv(2048)
            except:
                print('Connection to server lost.')
                return
            if data == '':
                print('Connection to server lost.')
                return
            msg = json.loads(str(data.decode('utf-8')))
            self.process_msg(msg)
        self.send_msg({'type': 'disconnect', 'data': None})

    def process_msg(self, msg):
        """Process the message from the server."""
        msgtype, msgdata = msg['type'], msg['data']
        if msgtype == 'playerlist':
            print('Players:', msg['data'])
        elif msgtype == 'begin_battle':
            self.turn = msgdata['turn']
            print('Turn:', self.turn)
            if self.turn == self.name:
                self.attack()
        elif msgtype == 'attack_result':
            print('Hit!' if msgdata['result'] else 'Miss!')
            self.turn = msgdata['turn']
            if self.turn == self.name:
                self.attack()
            print('Turn:', msgdata['turn'])
        elif msgtype == 'verdict':
            if msgdata['result'] == 'win':
                print("You win!")
            elif msgdata['result'] == 'lose':
                print("You lose!")
            self.game_finished = True

    def attack(self):
        """Attack the opponent at given position."""
        x, y = get_shot_coord().split(' ')
        self.send_msg({'type': 'attack', 'data': (x, y)})


def get_shot_coord():
    """Get shot coordinates from the user."""
    correct = False
    shot = None
    while not correct:
        shot = input('Enter shot coordinates in a form "x y": ')
        if len(shot.split(" ")) != 2 or not all(coord.isdigit() for coord in shot.split(" ")):
            print('Wrong shot coordinates.')
        else:
            correct = True
    return shot


client = Client(HOST, PORT)
client.start()
