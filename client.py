import socket, sys
from unit import *
from board import Board
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
        self.board = Board() 

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
    c1.board.add(Knight(), 2, 3)
    c1.board.add(Knight(), 4, 5)
    
    c2 = Client(HOST, PORT)
    c2.board.add(Knight(), 5, 8)
    c2.board.add(Knight(), 7, 9)
    
    c1.send(f"find||{c1.board.units[0]}")
    c2.send(f"find||{c2.board.units[0]}")
