import socket


class Client:
    def __init__(self):
        self.host, self.port = get_server_info()
        self.connected = False
        self.socket = None
        self.player_no = None

    def connect(self):
        """Try connecting to the server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            return True
        except socket.error as exception:
            print("socket.error exception:", exception)
            return False

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
                self.socket.sendall(input().encode('utf-8'))


def get_server_info():
    """Get server hostname and port from user."""
    host = input("Enter server hostname or IP address (enter nothing for 127.0.0.1): ")
    if not host:
        host = '127.0.0.1'
    port = input("Enter port (enter nothing for 12345): ")
    if not port:
        port = 12345
    return host, int(port)


if __name__ == "__main__":
    try:
        client = Client()
        client.connect()
        client.player_init()
        client.loop()
        client.socket.close()
    except KeyboardInterrupt:
        client.socket.close()


