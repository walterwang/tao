from pprint import pprint
from unit import *
import unit

class Board:
    def __init__(self, board_dict=None):
        self.units = [{},{}]
        self.pop_count = [0,0]
        self.coord = {}
        for x in range(0, 11):
            for y in range(0, 11):
                self.coord[(x, y)] = None
        if board_dict:
            for player, units in board_dict.items():
                self.add_units(units, player)

    
    def add(self, unit, x, y, p=0, uid=None):
        try:
            self.check_add(unit, x, y, p)
        except Exception as e:
            print('Failed to add {}, error {}'.format(unit, e))
            return
        
        self.pop_count[p] += unit.pop
        unit.pos = [x, y]
        unit.player = p
        unit.orient = [0, -1+p*2]
        
        unit.uid = uid if uid else self._get_uid(p)
        unit._hp.create_self_remove(self.remove, uid, p)
        self.units[p][unit.uid] = unit
        self.update(p)
        self.coord[(x, y)] = unit

    def add_units(self, units, player):

        for uid, u in units.items():

            self.add(getattr(unit, u['id'])(), u['pos'][0], u['pos'][1],
                           p=player, uid=uid)
    
    def remove(self, uid, p):
        print('units', self.units)
        print('uid, p', uid, p)
        self.pop_count[p] -= self.units[p][uid].pop
        self.coord[tuple(self.units[p][uid]._pos)]= None
        self.units[p].pop(uid)

        # del self.units[p][uid].pos
        # del self.units[p][uid].orient
        self.update(p)            

    def check_add(self, unit, x, y, p):
        if unit.pop + self.pop_count[p] > 10:
            raise Exception('pop limit reached')
        for u in self.units[p].values():
            if u.pos == [x, y]:
                raise Exception('{}, {} is occupied by {}'.format(
                    x, y, u))

    def update(self, p):
        for u in self.units[p].values():
            u.update_interactions(list(self.units[p].values()))

    def _get_uid(self, p):
        for i in range(1,100):
            if i not in self.units[p]:
                return i
    
    def change(self, player, uid, field, newvalue):
        setattr(self.units[player][uid], field, newvalue)

    def serialize(self):
        board = {}
        return board

    def pprint(self):
        pprint(self.units)
