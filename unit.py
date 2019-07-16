from config import Config
from board import Board

UNITS = Config('default.yml').units


class Unit:
    def __init__(self, id):
        setattr(self, id, UNITS[id])
        self.id = id
        self.uid = ''
        self.owner = ''
        self.pos = ''
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

if __name__ == '__main__':
    b = Board()
    
    k1 = Knight()
    p1 = Pyro()
    d1 = Dragon()
    dp = Dpyro()
    b.add(k1, 1, 3)
    b.add(p1, 3, 5)
    b.add(d1, 5, 2)
