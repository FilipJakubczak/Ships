import socket


class Client:
    def __init__(self):
        self.host, self.port = get_server_info()
        self.connected = False
        self.socket = None
        self.player_no = None

    def connect(self):
        """Connect to the server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print("Connected to:", self.host, "at", self.port)

    def player_init(self):
        """Set player nick and receive player number."""
        nick = bytes(input('Your nickname: '), 'utf-8')
        self.socket.sendall(nick)
        self.player_no = self.socket.recv(1024).decode('utf-8')

    def loop(self):
        """<TODO>"""
        while True:
            turn = self.socket.recv(1024).decode('utf-8')
            if turn == self.player_no:
                print('Your turn!')
                self.socket.sendall(get_shot_coord())


def get_server_info():
    """Get server hostname and port from the user."""
    host = input("Enter server hostname or IP address (enter nothing for 127.0.0.1): ")
    if not host:
        host = '127.0.0.1'
    port = input("Enter port (enter nothing for 12345): ")
    if not port:
        port = 12345
    return host, int(port)


def get_shot_coord():
    """Get shot coordinates from the user."""
    correct = False
    shot = None
    while not correct:
        shot = input("Enter shot coordinates in a form \"x y\": ")
        if len(shot.split(" ")) != 2 or not all(coord.isdigit() for coord in shot.split(" ")):
            print("Wrong shot coordinates.")
        else:
            correct = True
    return shot.encode('utf-8')


if __name__ == "__main__":
    try:
        client = Client()
        client.connect()
        client.player_init()
        client.loop()
        client.socket.close()
    except KeyboardInterrupt:
        client.socket.close()
    except socket.error as exception:
        print("Connection error:", exception)


