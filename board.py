class Board:
    def __init__(self):
        self.units = [{},{}]
        self.pop_count = [0,0]


    def add(self, unit, x, y, p=0, uid=None):
        try:
            self.check_add(unit, x, y, p)
        except Exception as e:
            print('Failed to add {}, error {}'.format(unit, e))
            return
        
        self.pop_count[p] += unit.pop
        unit.pos = [x, y]
        unit.orient = [0, -1+p*2]
        
        unit.uid = uid if uid else self._get_uid(p)
        self.units[p][unit.uid] = unit
        self.update(p)

    def remove(self, uid, p):
        self.pop_count[p] -= self.units[p][uid].pop
        self.units[p].pop(uid)
        del self.units[p][uid].pos
        del self.units[p][uid].orient
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
    
    def serialize(self):
        board = {}

        return board
