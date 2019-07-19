from threading import Thread
from random import shuffle
from board import Board

import unit
from unit import *

def check_valid(fn):
    def wrapper(*args, **kwargs):
        self = args[0]
        action = args[1]
        player = args[2]

        if not self.active_unit:
            self.active_unit = self.board.units[player][action['uid']]
        elif self.active_unit is not self.board.units[player][action['uid']]:
            print('wrong active unit')
            return
        fn(*args, **kwargs)
        self.update_players(action)
    return wrapper

class Game(Thread):
    def __init__(self, p0_handler, p1_handler):
        self.players = [p0_handler, p1_handler]
        shuffle(self.players)
        
        self.board = Board()
        self.board.add_units(self.players[0].units, 0)
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
            for player, handler in enumerate(self.players):
                while self.has_actions:
                    action = handler.command.get()
                    self.cmd.get(action['type'], 'nocmd')(action, player)

    def update_players(self, msg):
        for handler in self.players:
            handler.send(msg)
    
    def is_blocked(self, attacker, target):
        return None

    @check_valid
    def move(self, action, player):
        self.active_unit.pos = action['pos']
        # self.board[player][action['uid']].orient = action['orient']
    
    @check_valid
    def attack(self, action, player):
        for target in self.board[player][action['targets']]:
            # assign target with target object in the decorator

            if self.active_unit.blockable:
                if self.is_blocked(self.active_unit, target):
                    pass
            else:
                target.hp = target.hp - self.active_unit.dmg


#class Game:
#    def __init__(self, p0, p1):
#        self.gs = cycle(['1_move',
#                         '1_att',
#                         '1_orient',
#                         '2_move',
#                         '2_att',
#                         '2_orient'])
#        # p0.board.add_wait_time()
#        p1.board.reverse_board()
#        self.p = {0: p0,
#                  1: p1}
#        self.punit = { 0: p0.board.units.values(), 
#                       1: p1.board.units.values()}
#        self.all_units = p0.board.units.values().extend(p1.board.units.values())
#    
#    def start(self): 
#        next(self.gs)
#    
#    def get_active_unit(self, player, unit):
#        try:
#            return self.p[player].board.units[unit]
#        except Exception as e:
#            print(e)
#            raise Exception('no active unit')
#
#
#    def move(self, player, unit, path):
#        # check if there is a unit
#        a_unit = self.get_active_unit(player, unit)
#        self.check_valid_path(player, a_unit, path)
#        a_unit.pos = path[-1]
#    
#    def attack(self, player, unit, target):
#        targets = [target]
#        a_unit = self.get_active_unit(player, unit)
#        target = a_unit.getlos(target)
#        targets = a_unit.getaoe(target) 
#        for t in targets:
#            for u in self.all_units:
#                if t == u.pos:
#                    self.calc_dmg(a_unit, u)
#
#    def calc_dmg(self, attacker, defender):
#        defender.hp -= attacker.dmg
#    
#    def orient(self, player, unit, orient):
#        a_unit = self.get_active_unit(player, unit)
#        # check if valid orientation
#        a_unit.orient = orient
#
#    def check_valid_path(self, player, a_unit, path):
#        if len(path) > a_unit.movement:
#            raise Exception('{} too many moves'.format(a_unit))
#        for ind, p in enumerate(path):
#            for u in self.punit[player]:
#                if p == u.pos and (u.untamed or ind == len(path)-1):
#                    raise Exception('{} path is blocked by {}'.format(a_unit, u))
#            for u in self.punit[1^player]:
#                if p == u.pos:
#                    raise Exception('{} path is blocked by {}'.format(a_unit, u))
    




        


