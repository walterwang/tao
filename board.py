class Board:
    def __init__(self):
        self.units = {}
        "objects to be updated"
        self.pop_count = 0

    def add(self, unit):
        if unit.pop + self.pop_count > 10:
            return 'pop limit reached'
        self.pop_count += unit.pop
        unit.uid = self._get_uid()
        self.units[unit.uid] = unit
        self.update()

    def remove(self, uid):
        self.pop_count -= self.units[uid].pop
        self.units.pop(uid)
        self.update()            

    def update(self):
        for u in self.units.values():
            u.update_interactions(list(self.units.values()))

    def register(self):
        pass

    def _get_uid(self):
        for i in range(1,100):
            if i not in self.units:
                return i
        
