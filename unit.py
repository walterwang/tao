from config import Config
from math import ceil

import random
UNITS = Config('default.yml').units


class Hp:
    def __init__(self, hp, armor_obj):
        self._hp = int(hp)
        self.armor = armor_obj
    
    def __sub__(self, dmg):
        self._hp -= dmg - (self.armor * dmg)
        if self._hp <= 0:
            self._remove(self.uid, self.p)
        
    def __add__(self, heal):
        self._hp += heal
    
    def __repr__(self):
        return repr(self._hp)
    
    def create_self_remove(self, remove_func, uid, p):
        self._remove = remove_func
        self.uid = uid
        self.p = p

class Armor:
    def __init__(self, armor):
        self._armor = int(armor) / 100

    def __add__(self, value):
        self._armor += (value / 100)

    def __sub__(self, value):
        self._armor -= (value / 100)

    def __mul__(self, dmg):
        return int(dmg * self._armor)

    def __repr__(self):
        return repr(self._armor * 100)

class Unit:
    def __init__(self, id):
        self.id = id
        self.uid = ''
        self.player = None
        self._pos = None
        self._orient = ''
        self.wait_times = 0
        self.wait = None
        self.teleport = False
        self.movement = None
        self.blockable = None
        self.dmg = None
        setattr(self, id, UNITS[id])
    
    def __setattr__(self, k, val):
        if isinstance(val, dict):
            for k, v in val.items():
                setattr(self, k, v)
        else:
            super().__setattr__(k, val)
    
    def __repr__(self):
        return f"{{'id':'{self.id}','pos':{self.pos}}}"
    
    def __eq__(self, string):
        if string == self.id:
            return True
        return False
        
    def update_interactions(self, units):
        pass

    def getaoe(self, target):
        return [target]

    def getlos(self, target):
        return target

    def resetattr(self, attr):
        setattr(self, attr, UNITS[self.id]['stats'][attr])
    
    def attack(self, target=None, coord=None, targets=None):
        changes = []
        self.wait_times += ceil(self.wait/2)
        self.set_new_orient(target)
        if not targets:
            targets = self.attack_pattern(target, coord)
        print(f'attack: {target},  {targets}')
        for target_unit, is_blocked in targets:
            if target_unit:
                result = self.attack_effect(target_unit, is_blocked)
                changes.append({'uid': target_unit.uid,
                                'player': target_unit.player,
                                'effect': result})
        return changes

    def attack_pattern(self, target, coord):
        if not target:
            return []
        return [[coord[target],None]]
    
    def attack_effect(self, target_unit, is_blocked):
        if is_blocked and is_blocked == 'blocked':
            return
        if is_blocked and is_blocked == 'unblocked':
            pass
        elif self.blockable and target_unit.fblock > 0:
            if self._orient == target_unit._orient:
                block_chance = target_unit.bblock
            elif (self._orient[0] + target_unit._orient[0]) == 0 \
                    and (self._orient[1] + target_unit._orient[1]) == 0:
                block_chance = target_unit.fblock
            else:
                block_chance = target_unit.sblock
            if random.random() < block_chance:
                return 'blocked'
        _ = target_unit.hp - self.dmg
        return 'unblocked' 
    
    def move(self, new_pos):
        self.wait_times += self.wait//2
        self._pos = new_pos

    def available_move(self, coord):
        available_moves = {} # key is x,y, value is list of coord that is the path
        path = {}
        path[tuple(self._pos)] = []
        seed = [tuple(self._pos)]
        next_seed = []
        visited = set() # set of node that have been visited

        for i in range(0, self.movement):
            for s in seed:
                for pt in [(0,1), (1,0), (-1,0), (0,-1)]:
                    new_pos = (s[0] + pt[0], s[1] + pt[1])
                    if new_pos[0] > 10 or \
                            new_pos[1] > 10 or \
                            new_pos[0] < 0 or \
                            new_pos[1] < 0: 
                        continue
                    if new_pos in visited:
                        continue
                    visited.add(new_pos)
                    if self.unmovable(new_pos, coord):
                        continue
                    path[new_pos] = path[s].copy()
                    path[new_pos].append(new_pos)
                    next_seed.append(new_pos)
                    if not coord[new_pos]:
                        available_moves[new_pos] = path[s]
            seed = next_seed.copy()
            next_seed = [] 
        return available_moves
    
    def unmovable(self, pos, coord):
        if not coord[pos]:
            return False
        if coord[pos].player != self.player or coord[pos].untamed:
            return True
        return False 
    @property
    def armor(self):
        return self._armor
    @armor.setter
    def armor(self, value):
        self._armor = Armor(value)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = Hp(value, self.armor)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new_pos):
        self.set_new_orient(new_pos)
        self._pos = new_pos

    @property
    def orient(self):
        return self._orient

    @orient.setter
    def orient(self, value):
        self._orient = value
    
    def set_new_orient(self, new_pos):
        if self._pos:
            x = new_pos[0] - self._pos[0]
            y = new_pos[1] - self._pos[1]
            if abs(x) >= abs(y):
                x_orient = x/abs(x)
                y_orient = 0
            else:
                x_orient = 0
                y_orient = y/abs(y)
            self._orient = [x_orient, y_orient]


class Knight(Unit):
    def __init__(self):
        super().__init__('Knight')
    
    
class Pyro(Unit):
    def __init__(self):
        super().__init__('Pyro')

    def update_interactions(self, units):
        if 'Dpyro' in units and 'Dragon' in units:
            self.dmg = UNITS['Pyro']['stats']['dmg'] + \
                    UNITS['Dragon']['stats']['dmg'] // \
                    (units.count('Pyro') + units.count('Dpyro'))
        else:
            self.resetattr('dmg')

class Dpyro(Unit):
    def __init__(self):
        super().__init__('Dpyro')

    def update_interactions(self, units):
        if 'Dpyro' in units and 'Dragon' in units:
            self.dmg = UNITS['Pyro']['stats']['dmg'] + \
                    UNITS['Dragon']['stats']['dmg'] // \
                    (units.count('Pyro') + units.count('Dpyro'))

        else:
            self.resetattr('dmg')

class Dragon(Unit):
    def __init__(self):
        super().__init__('Dragon')

    def update_interactions(self, units):
        if 'Dpyro' in units:
            self.dmg = UNITS['Dragon']['stats']['dmg'] // \
                    (units.count('Pyro') + units.count('Dpyro'))

        else:
            self.resetattr('dmg')

