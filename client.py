import socket, sys

HOST, PORT = "localhost", 9999

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message.encode())
        response = sock.recv(1024)
        print('Recieved: {}'.format(response))
    finally:
        sock.close()
if __name__ == '__main__':
    client(HOST, PORT, "Hello world 1")
