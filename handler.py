from queue import Queue
from threading import Thread
from ast import literal_eval
import random

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class Handler:
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.recv = request_handler.request.recv
        self.game = request_handler.game
        
        self.in_game = False 
        
        self.command = Queue()
        self.recieve = Queue()
       
        self.session_id = random.randint(1,10000)

        self.cmd = {b'find': self.find,
                    b'canc': self.canc,
                    b'quit': self.quit,
                    b'form': self.form,
                    b'move': self.move}

    def __call__(self):
        while True:
            data = self.recv(1024).split(b'||')
            r = self.cmd.get(data[0],
                             self.nocmd)(literal_eval(data[1].decode()))
            self.send(r)
            
    def send(self, msg):
        msg = bytes(msg, encoding='utf-8')
        self.request_handler.request.sendall(msg)


    def find(self, units):
        print(units)
        self.units = units 
        self.game[self.session_id] = self
        ## game dict is monitored by matchmaker 
        return 'inqueue'

    def canc(self, *args):
        try:
            self.game.pop(self.session_id)
        except:
            return 'game not found'
        return 'cancelled'
    
    def quit(self, *args):
        return 'quit'

    def form(self, *args):
        pass

    def move(self, data):
        self.command.put(data[1])
        return self.recieve.get()

    def nocmd(self, data):
        return b'command not found'
    
