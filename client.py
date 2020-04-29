import socket
import threading as thread
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12340       # The port used by the server

# def get_message(sock):
#     while True:
#         data = sock[0].recv(1024)
#         if not data:
#             continue
#         print(data.decode('utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # thread.Thread(target=get_message, args=[s]).start()
    nick = bytes(input('Your nickname: '), 'utf-8')
    s.sendall(nick)
    player_no = s.recv(1024).decode('utf-8')
    while True:
        turn = s.recv(1024).decode('utf-8')
        if turn == player_no:
            print('Your turn!')
            s.sendall(input().encode('utf-8'))
        


