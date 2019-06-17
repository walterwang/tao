class Board:
    def __init__(self):
        self.units = {}
        self.pop_count = 0

    def add(self, unit, x, y):
        try:
            self.check_add(unit, x, y)
        except Exception as e:
            print('Failed to add {}, error {}'.format(unit, e))
            return
        self.pop_count += unit.pop
        unit.pos = [x, y]
        unit.orient = [1, 1]
        unit.uid = self._get_uid()
        self.units[unit.uid] = unit
        self.update()

    def remove(self, uid):
        self.pop_count -= self.units[uid].pop
        self.units.pop(uid)
        del self.units[uid].pos
        del self.units[uid].orient
        self.update()            

    def check_add(self, unit, x, y):
        if unit.pop + self.pop_count > 10:
            raise Exception('pop limit reached')

        for u in self.units.values():
            if u.pos == [x, y]:
                raise Exception('{}, {} is occupied by {}'.format(
                    x, y, u))

    def update(self):
        for u in self.units.values():
            u.update_interactions(list(self.units.values()))

    def reverse_board(self):
        " for player 2, y is flipped and orientation is flipped"
        for u in self.units.values():
            u.pos = [u.pos[0], -u.pos[1]]
            u.orient = [u.orient[0], -u.orient[1]]

    def _get_uid(self):
        for i in range(1,100):
            if i not in self.units:
                return i
        
