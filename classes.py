import threading as th
import socket
import numpy as np


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.ships_player1 = []
        self.ships_player2 = []
        self.fields_attacked_player1 = []
        self.fields_attacked_player2 = []

    def check_result(self):
        if not self.ships_player1:
            return self.player2, self.player1
        if not self.ships_player2:
            return self.player1, self.player2

        return None, None

    def attack(self, attacker, field):
        if attacker == self.player1:
            board = self.ships_player2
            fields_attacked = self.fields_attacked_player2
        else:
            board = self.ships_player1
            fields_attacked = self.fields_attacked_player1

        if field not in fields_attacked:
            fields_attacked.append(field)
            if field in board:
                board.remove(field)
                print('field:', field, ' Board:', board)
                return True
        else:
            print('Field already attacked!')
        return False

    def place_ship(self, player, n=1, pos=None):
        if pos == None:
            pos = (np.random.randint(0, 10), np.random.randint(0, 10))
        if player == self.player1:
            self.ships_player1.append(pos)
        else:
            self.ships_player2.append(pos)
    
    def print_board(self, player):
        if player == self.player1:
            ships = self.ships_player1
            name = self.player1.name
        else:
            ships = self.ships_player2
            name = self.player2.name
        print(name + "'s board:")
        print(' ', end='   ')
        for x in range(10):
            print(x, end='   ')
        print('\n')
        for y in range(10):
            print(y, end='   ')
            for x in range(10):
                if (x, y) in ships:
                    print('#', end='   ')
                else:
                    print(' ', end='   ')
            print('\n')

class Player(dict):
    def __init__(self, sock, name):
        dict.__init__(self, fname=name)
        self.sock = sock
        self.name = name

    def __repr__(self):
        return repr(self.name)

