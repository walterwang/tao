from queue import Queue
import random

class Handler:
    def __init__(self, request_handler):
        self.recv = request_handler.request.recv
        self.send = request_handler.request.sendall
        self.game = request_handler.game
        self.begn = request_handler.begin_game
        
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
            self.cmd.get(data[0], self.nocmd)(data)
            if self.begn:
                
                self.send(self.recieve.get())
            
                
            
            
    def find(self, *args):
        self.game[self.session_id]=(self.command, self.recieve)

    def canc(self, *args):
        self.game.pop(self.session_id)

    def quit(self, *args):
        pass

    def form(self, *args):
        pass

    def move(self, data):
        self.command.put(data[1])
        self.send(self.recieve.get())


    def nocmd(self, data):
        print('command not found')



