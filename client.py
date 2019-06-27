import socket, sys

HOST, PORT = "localhost", 9999

class Client:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def send(self, message):
        try:
            self.sock.sendall(message.encode())
            response = self.sock.recv(1024)
            print('Recieved: {}'.format(response))
        except:
            pass

    def close(self):
        self.sock.close()

if __name__ == '__main__':
    c1 = Client(HOST, PORT)
    c2 = Client(HOST, PORT)
    c1.send('ready')

