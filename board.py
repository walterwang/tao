class Board:
    def __init__(self):
        self.units = {}
        "objects to be updated"
        self.pop_count = 10

    def add(self, unit):
        if unit.pop + self.pop_count > 10:
            return 'pop limit reached'
        self.pop_count += unit.pop
        unit.uid = self.pop_count
        self.units[unit.uid] = unit
        self.update()

    def remove(self, uid):
        self.units.pop(uid)

    def update(self):
        for u in self.units.values():
            u.update_interactions(list(self.units.values()))

    def register(self):
        pass
        
