from itertools import cycle


class Game:
    def __init__(self, p0, p1):
        self.gs = cycle(['1_move',
                         '1_att',
                         '1_orient',
                         '2_move',
                         '2_att',
                         '2_orient'])
        # p0.board.add_wait_time()
        p1.board.reverse_board()
        self.p = {0: p0,
                  1: p1}
        self.punit = { 0: p0.board.units.values(), 
                       1: p1.board.units.values()}
        self.all_units = p0.board.units.values().extend(p1.board.units.values())
    
    def start(self): 
        next(self.gs)
    
    def get_active_unit(self, player, unit):
        try:
            return self.p[player].board.units[unit]
        except Exception as e:
            print(e)
            raise Exception('no active unit')


    def move(self, player, unit, path):
        # check if there is a unit
        a_unit = self.get_active_unit(player, unit)
        self.check_valid_path(player, a_unit, path)
        a_unit.pos = path[-1]
    
    def attack(self, player, unit, target):
        targets = [target]
        a_unit = self.get_active_unit(player, unit)
        if a_unit.los:
            target = a_unit.getlos(target)
        if a_unit.aoe:
            targets = 
        for u in self.all_units:
            

    def check_valid_path(self, player, a_unit, path):
        if len(path) > a_unit.movement:
            raise Exception('{} too many moves'.format(a_unit))
        for ind, p in enumerate(path):
            for u in self.punit[player]:
                if p == u.pos and (u.untamed or ind == len(path)-1):
                    raise Exception('{} path is blocked by {}'.format(a_unit, u))
            for u in self.punit[1^player]:
                if p == u.pos:
                    raise Exception('{} path is blocked by {}'.format(a_unit, u))
    




        


