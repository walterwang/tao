import traceback
import unit
from unit import *

from threading import Thread
from random import shuffle
from board import Board

def check_valid(fn):
    def wrapper(*args, **kwargs):
        self = args[0]
        action = args[1]
        player = args[2]
        if action['type'] != 'wait':
            if not self.active_unit:
                self.active_unit = self.board.units[player][action['uid']]
                if self.active_unit.wait_times > 0:
                    return
            elif self.active_unit is not self.board.units[player][action['uid']]:
                print('wrong active unit')
                return
        print(action, player)
        changes = fn(*args, **kwargs)
        if action['type'] in ['orient', 'wait']:
            player = (player + 1) % 2
        self.update_players(changes, player)
    return wrapper

class Game(Thread):
    def __init__(self, p0_handler, p1_handler):
        self.players = [p0_handler, p1_handler]
        shuffle(self.players)
        
        self.board = Board()
        self.board.add_units(self.players[0].units, 0)
        
        for _, unit in self.players[1].units.items():
            unit['pos'][1] = 10 - unit['pos'][1]
 
        self.board.add_units(self.players[1].units, 1)
        
        print('board created')
        print(self.board.units)
        self.players[0].send(f'begin||0||{self.board.units}')
        self.players[1].send(f'begin||1||{self.board.units}')

        self.game_going = True
        self.has_actions = True
        self.active_unit = None
        self.cmd = {
                    'move': self.move,
                    'attack': self.attack,
                    'orient': self.orient,
                    'wait': self.wait,
                    'nocmd': self.nocmd
                   }
        Thread.__init__(self)
           
                
    def run(self):
        while self.game_going:
            try:
                for player, handler in enumerate(self.players):
                    while self.has_actions:
                        print(f'______player {player} turn____________')
                        action = handler.command.get()
                        self.cmd.get(action['type'], 'nocmd')(action, player)
                    self.has_actions = True
                    self.active_unit = None
            except Exception as e:
                print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
                print('player disconnected')
                break

    def update_players(self, msg, player):
        msg = f"update||{player}||{msg}"
        for handler in self.players:
            handler.send(msg)
    
    def is_blocked(self, attacker, target):
        return None

    @check_valid
    def move(self, action, player):
        self.active_unit.move(action['pos'])
        changes = {'player': player,
                'uid': action['uid'],
                'type': 'move',
                'pos': action['pos']}
        return changes
    
    @check_valid
    def attack(self, action, player):
        print('self active unit: ', self.active_unit)
        targets = self.active_unit.attack(target=action['target'],
                                          coord=self.board.coord)
        changes = {'player': player, 
                   'uid': action['uid'],
                   'type': 'attack',
                   'target': str(action['target']),
                   'targets': str(targets)}
        return changes

    @check_valid
    def orient(self, action, player):
        print('orient: ', action['orient'])
        self.active_unit.orient = action['orient']
        self.has_actions = False
        changes = {'player': player,
                   'uid': action['uid'],
                   'type': 'orient',
                   'orient': action['orient']}
        return changes

    @check_valid
    def wait(self, action, player):
        changes = {'player': player,
                   'type': 'wait'}
        self.has_actions = False
        return changes

    def nocmd(self, action, player):
        pass


        


