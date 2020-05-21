"""Filip Jakubczak, Łukasz Łapiński"""

import threading as thread
import socket
import json
import sys
from classes import Player, Game


playerlist = []
threads = []
game = None

def start_game():
    """Funkcja rozpoczynająca grę."""
    global game
    player1, player2 = playerlist[0], playerlist[1]
    game = Game(player1, player2)
    for i in range(2):
    	game.place_ship(player1)
    	game.place_ship(player2)
    game.print_board(player1)
    game.print_board(player2)
    if len(game.ships_player1) != 0 and len(game.ships_player2) != 0:
            dictData = {
                'type': 'begin_battle',
                'data': {
                    'shipData': {
                        game.player1.name: game.ships_player1,
                        game.player2.name: game.ships_player2,
                    },
                    'turn': game.player1.name
                }
            }
            json_data = json.dumps(dictData)

            send_message(json_data, game.player1)
            send_message(json_data, game.player2)

def send_message(msg, target):
    """Funkcja wysyłająca wiadomość w formacie JSON do klienta."""
    target.sock.send(msg.encode('utf-8'))

def process_message(player, msgtype, msgdata):
    """Funkcja przetwarzająca wiadomość JSON od serwera."""
    global playerlist, game

    if msgtype == 'connect':
        return client_connect(player, msgdata)

    elif msgtype == 'disconnect':
        print(msgdata, 'has disconnected.')
        player.sock.close()
        if player in playerlist:
            playerlist.remove(player)
        
    elif msgtype == 'attack':
        print('Attack!')
        msgdata = tuple(map(int, msgdata))
        result = game.attack(player, msgdata)

        winner, loser = game.check_result()
        if winner is not None and loser is not None:
            msg_winner = {
                'type': 'verdict', 'data': {'result': 'win'}}
            msg_loser = {
                'type': 'verdict', 'data': {'result': 'lose'}}
            msg_winner = json.dumps(msg_winner)
            msg_loser = json.dumps(msg_loser)

            send_message(msg_winner, winner)
            send_message(msg_loser, loser)
        else:
            if player.sock == game.player1.sock:
                turn = game.player2.name
            else:
                turn = game.player1.name
            print('Turn:', turn)
            dictData = {
                'type': 'attack_result',
                'data': {
                    'result': result,
                    'turn': turn
                }
            }
            json_data = json.dumps(dictData)

            send_message(json_data, game.player1)
            send_message(json_data, game.player2)
    else:
        print('Invalid message type.')

def client_connect(client, name):
    """Funkcja łącząca serwer z klientem."""
    player = Player(client, name)
    playerlist.append(player)
    print(player.name, 'has connected.')
    msgdata = {'type': 'playerlist', 'data': playerlist}
    msg = json.dumps(msgdata)

    for player in playerlist:
        send_message(msg, player)

    return player

def handle_client(client):
    """Funkcja nasłuchująca wiadomości od klienta i obsługująca je."""
    while True:
        if isinstance(client, Player):
            try:
                data = client.sock.recv(2048)
            except:
                print(client.name, 'has disconnected.')
                return
            if data == '':
                print(client.name, 'has disconnected.')
                client.sock.close()
                if client in playerlist:
                    playerlist.remove(client)
                return
        else:
            data = client.recv(2048)
            if data == '':
                client.close()
                return

        if not data:
            continue
        message = json.loads(str(data.decode('utf-8')))
        msgtype = message['type']
        msgdata = message['data']
        if isinstance(client, Player):
            process_message(client, msgtype, msgdata)
        else:
            client = process_message(client, msgtype, msgdata)
        if game is None and len(playerlist) == 2:
            start_game()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    host = input('Enter server hostname or IP address (enter nothing for 127.0.0.1): ')
    if not host:
        host = '127.0.0.1'
    port = input('Enter port (enter nothing for 12345): ')
    if not port:
        port = 12345
    try:
        server_socket.bind((host, port))
        print('Server started...')
    except Exception as e:
        print(e)
        print('Cannot start server.')
        sys.exit(1)
    server_socket.listen(2)
    clients = 0
    while True:
        client, address = server_socket.accept()
        clients += 1
        th = thread.Thread(target=handle_client, args=(client,))
        threads.append(th)
        th.start()
        if clients == 2:
            break
    for th in threads:
        th.join()
