from queue import Queue
from threading import Thread
import random

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class Handler:
    def __init__(self, request_handler):
        self.recv = request_handler.request.recv
        self.send = request_handler.request.sendall
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
            data = self.recv(1024).split(b' ')
            print(data)
            r = self.cmd.get(data[0], self.nocmd)(data)
            self.send(r)
            
    def find(self, *args):
        self.game[self.session_id] = self
        ## game dict is monitored by matchmaker 
        return b'in queue'

    def canc(self, *args):
        try:
            self.game.pop(self.session_id)
        except:
            return b'game not found'
        return b'cancelled'
    
    def quit(self, *args):
        return b'quit'

    def form(self, *args):
        pass

    def move(self, data):
        self.command.put(data[1])
        return self.recieve.get()

    def nocmd(self, data):
        return b'command not found'
    
    def game_start(self, game_init):
        # method called by matchmaker, to notify start of game
        self.send(game_init)

