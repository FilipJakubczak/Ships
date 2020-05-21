"""Filip Jakubczak, Łukasz Łapiński"""

import socket
import threading as thread
import json
import sys


class Client:
    def __init__(self, host, port):
        self.host, self.port = host, port
        self.sock = None
        self.name = None
        self.game_finished = False
        self.turn = None

    def start(self):
        """Funkcja dołączająca klienta do gry."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.sock = s
            self.connect()
            self.set_name()
            self.send_msg({'type': 'connect', 'data': self.name})
            listener = thread.Thread(target=self.listener)
            listener.start()
            listener.join()

    def connect(self):
        """Funkcja łącząca się z serwerem za pomocą gniazda."""
        try:
            self.sock.connect((self.host, self.port))
        except Exception as ex:
            print(ex)
            print('Could not connect to server.')
            sys.exit(1)
        print('Connected to server.')

    def set_name(self):
        """Funkcja ustawiająca nazwę gracza."""
        nick = input('Your nickname: ')
        self.name = nick

    def send_msg(self, msg):
        """Funkcja wysyłająca wiadomość w formacie JSON do serwera."""
        msg = json.dumps(msg)
        self.sock.send(msg.encode('utf-8'))

    def listener(self):
        """Funkcja nasłuchująca wiadomości od serwera."""
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
        """Funkcja przetwarzająca wiadomość JSON od serwera."""
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
        """Funkcja do atakowania planszy przeciwnika."""
        x, y = get_shot_coord().split(' ')
        self.send_msg({'type': 'attack', 'data': (x, y)})


def get_shot_coord():
    """Funkcja pomocnicza do pobrania współrzędnych ataku od użytkownika."""
    correct = False
    shot = None
    while not correct:
        shot = input('Enter shot coordinates in a form "x y": ')
        if len(shot.split(" ")) != 2 or not all(coord.isdigit() for coord in shot.split(" ")):
            print('Wrong shot coordinates.')
        else:
            correct = True
    return shot


host = input('Enter server hostname or IP address (enter nothing for 127.0.0.1): ')
if not host:
    host = '127.0.0.1'
port = input('Enter port (enter nothing for 12345): ')
if not port:
    port = 12345
client = Client(host, port)
client.start()
