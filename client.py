import ast
import socket
from unit import * 
from board import Board
from queue import Queue
from threading import Thread
from ast import literal_eval

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
        self.current_turn = 0
        self.action = {'move': self.move_unit,
                       'attack': self.attack_unit,
                       'orient': self.orient_unit}
    def send(self, message):
        try:
            self.sock.sendall(message.encode())
        except:
            pass

    def close(self):
        self.sock.close()
    
    def begin(self, args):
        self.player = int(args[0])
        p1_units, p2_units = ast.literal_eval(args[1])
        self.board = Board(board_dict = {0:p1_units, 1:p2_units})
        
    def find(self):
        self.send(f"find||{self.board.units[0]}")
    
    def inqueue(self, args):
        print('player in queue')
    
    def move(self, m):
        if self.player == self.current_turn:
            self.send(f"move||{m}")

    def update(self, args):
        self.current_turn = int(args[0])
        ad = ast.literal_eval(args[1])
        if ad['type'] == 'wait':
            return
        active_unit = self.board.units[ad['player']][ad['uid']]
        self.action.get(ad['type'])(active_unit, ad)
    
    def move_unit(self, active_unit, action_dict):
        active_unit.move(action_dict['pos'])

    def attack_unit(self, active_unit, ad):
        targets = ast.literal_eval(ad['targets'])
        target = ast.literal_eval(ad['target'])
        target = (int(target[0]), int(target[1]))
        server_targets = []
        for t in targets:
            target_unit = self.board.units[t['player']][t['uid']]
            server_targets.append([target_unit, t['effect']])
        active_unit.attack(target=target,
                           coord=self.board.coord,
                           targets=server_targets)
    
    def orient_unit(self, active_unit, ad):
        active_unit.orient=ad['orient']

    
    @threaded
    def recieve(self):
        while True:
            r = self.sock.recv(1024).decode()
            if r: 
                r = r.split('||')
                getattr(self, r[0])(r[1:])
    

if __name__ == '__main__':
    c1 = Client(HOST, PORT)
    c1.board.add(Knight(), 2, 3)
    c1.board.add(Knight(), 4, 5)
    
    c2 = Client(HOST, PORT)
    c2.board.add(Knight(), 5, 8)
    c2.board.add(Knight(), 7, 9)
   
    c1.find()
    c2.find()
    
    c3 = Client(HOST, PORT)
    c3.board.add(Knight(), 5, 8)
    c3.board.add(Knight(), 7, 9)

    c4 = Client(HOST, PORT)
    c4.board.add(Knight(), 5, 8)
    c4.board.add(Knight(), 7, 9)
 
    att_action = {'type':'attack',
                  'uid': 1,
                  'target': (4,5)}
    move_action = {'type': 'move',
                   'uid': 1,
                   'pos': [0, 6]}

    orient_action = {'type':'orient',
                     'uid': 1,
                     'orient': [1, 0]}
    wait_action = {'type':'wait'}
