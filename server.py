import threading as th
import _thread as thread
import socket               # Import socket module
import numpy as np
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12340        # Port to listen on (non-privileged ports are > 1023)

class Client:
    def __init__(self, sock, addr, id):
        self.sock = sock
        self.addr = addr
        self.id = id
        self.nick = self.sock.recv(1024).decode('utf-8')

    def __repr__(self):
        return (self.sock, self.addr, self.nick, self.id)

    def is_connected(self):
        if not self.sock.recv(1024):
            return False
        return True

    def get_message(self):
        return self.sock.recv(1024)

    def send_message(self, msg):
        return self.sock.sendall(msg)

    def close_connection(self):
        self.sock.close()

    def set_board(self, width, height, n):
        self.board_ = Board(width, height)
        self.board_.fill_board(n)
        self.ships_ = n
    
    def get_board(self):
        return self.board_
    
    def sink_ship(self):
        self.ships_ -= 1

    def shoot(self, target, pos):
        if target.get_board().hit():
            target.sink_ship()

class Ship:
    def __init__(self):
        #TODO implement ship length
        self.sunk_ = False
    def __repr__(self):
        return 'x' if self.sunk_ else 'o'
    def is_sunk(self):
        return self.sunk_
    def sink(self):
        self.sunk_ = True

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board_ = np.array([['#' for _ in range(width)] for _ in range(height)], dtype=Ship)
    
    def place_ship(self, ship, pos = None):
        if pos == None:
            pos = (np.random.randint(0, self.width - 1), np.random.randint(0, self.height - 1))
        self.board_[pos] = Ship()
    
    def fill_board(self, n):
        for i in range(n):
            self.place_ship(Ship())

    def hit(self, pos):
        if type(self.board_[pos]) is Ship:
            if not self.board_[pos].is_sunk():
                self.board_[pos].sink()
                print('Hit!')
                return True
            else:
                print('The ship is already sunk!')
        else:
            print('Miss!')
        return False


    def print_board(self):
        print(' ', end='   ')
        for col_index, _ in enumerate(self.board_):
            print(col_index, end='   ')
        print('\n')
        for row_index, row in enumerate(self.board_):
            print(row_index, end='   ')
            for element in row:
                print(element, end='   ')
            print('\n')

def client_connect(client, id):
    client.send_message(str(id).encode('utf-8'))
    print(client.nick, 'has joined as player {}.'.format(client.id))
    while True:
        if not client.is_connected():
            print(client.nick, 'has disconnected!')
            break
    client.close_connection()
    clients.remove(client)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print ('Server started!')
    print ('Waiting for clients...')
    clients = []
    s.bind((HOST, PORT))
    s.listen(2)
    threads = []
    for id in range(1, 3):
        c, addr = s.accept()
        client = Client(c, addr, id)
        clients.append(client)
        threads.append(th.Thread(target=client_connect, args=(client, id)).start())
    for id, client in enumerate(clients):
            client.set_board(5, 5, 2)
            print('Board of player {}:'.format(id + 1))
            client.get_board().print_board()
    turn = 0
    while th.active_count() == 3:
        player_turn = turn % 2 + 1
        if player_turn == 1:
            clients[0].send_message(str(player_turn).encode('utf-8'))
            print('Turn of Player 1')
            #TODO fix this
            while True:
                msg = clients[0].get_message().decode('utf-8')
                if len(msg) > 0:
                    hit_pos = tuple(msg.split(' '))
                    hit_pos = tuple(map(int, msg))
                    clients[1].shoot(target=clients[0], pos=hit_pos)
                    break
        else:
            clients[1].send_message(str(player_turn).encode('utf-8'))
            print('Turn of Player 2')
            #TODO fix this
            while True:
                msg = clients[1].get_message().decode('utf-8')
                if len(msg) > 0:
                    hit_pos = tuple(msg.split(' '))
                    hit_pos = tuple(map(int, msg))
                    clients[1].shoot(target=clients[0], pos=hit_pos)
                    break
        turn += 1
