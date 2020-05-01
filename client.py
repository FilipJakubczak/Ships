import socket
import threading as thread
import json
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12341       # The port used by the server

turn = None

def listener(sock):
    global turn
    while True:
        try:
            data = sock.recv(2048)
        except:
            print('Connection to server lost.')
            return
        if data == '':
            print('Connection to server lost.')
            return
        msg = json.loads(str(data.decode('utf-8')))
        msgtype = msg['type']
        msgdata = msg['data']
        if msgtype == 'playerlist':
            print('Players:', msg['data'])
        elif msgtype == 'begin_battle':
            turn = msgdata['turn']
            print('Turn:', msgdata['turn'])
            if turn == name:
                attack(sock)
        elif msgtype == 'attack_result':
            if msgdata['result']:
                print('Hit!')
            else:
                print('Miss!')
            turn = msgdata['turn']
            if turn == name:
                attack(sock)
            print('Turn:', msgdata['turn'])
        elif msgtype == 'verdict':
            if msgdata['result'] == 'win':
                print("You win!")
            elif msgdata['result'] == 'lose':
                print("You lose!")
            break
    
    send_msg(sock, {'type': 'disconnect', 'data': None})

def send_msg(sock, msg):
    msg = json.dumps(msg)
    sock.send(msg.encode('utf-8'))
    
def attack(sock):
    x, y = input('Attack position:').split(' ')
    send_msg(s, {'type': 'attack', 'data': (x, y)})

name = input('Your name: ')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print(e)
        print('Could not connect to server.')
        sys.exit(1)
    print('Connected to server.')
    send_msg(s, {'type': 'connect', 'data': name})
    listener = thread.Thread(target=listener, args=(s,))
    listener.start()
    listener.join()
    
    
    
        


