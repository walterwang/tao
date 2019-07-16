import socket, sys
from queue import Queue
from threading import Thread

HOST, PORT = "localhost", 9999


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class Client:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.queue = Queue()
        self.recieve()
        
    def send(self, message):
        try:
            self.sock.sendall(message.encode())
        except:
            pass

    def close(self):
        self.sock.close()

    @threaded
    def recieve(self):
        while True:
            self.queue.put(self.sock.recv(1024))
    
if __name__ == '__main__':
    c1 = Client(HOST, PORT)
    c2 = Client(HOST, PORT)
    c1.send('find')

