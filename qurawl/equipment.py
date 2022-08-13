"""
Equipment
"""

####

import os
from collections import defaultdict as defdict
import itertools as it


####

EQUIP_DEFAULT = 0
MAXIMA_DEFAULT = 1
PORTION = 1

####

def const_factory(value=0):

    return it.repeat(value).__next__

####

class Equipment(object):


    def __init__(self, maxima, equip):

        self.maxima = defdict(const_factory(MAXIMA_DEFAULT))
        self.maxima.update(maxima)
        self.equip = defdict(const_factory(EQUIP_DEFAULT))
        self.equip.update(equip)


    def pickup(self, gadget):

        name = gadget.name
        maximum = self.maxima[name]
        if self.equip[name] < maximum:
            val = gadget.value + self.equip[name]
            self.equip[name] = min(max(0, val), maximum)
            return True
        return False


    def laydown(self, name, portion=PORTION):

        if self.equip[name] >= portion:
            self.equip[name] -= portion
            return True
        return False


    def __repr__(self):
        return ' '.join("%s:%s" % (key, value) for key, value in\
                        sorted(self.equip.items()))

####

class Gadget(object):

    def __init__(self, name, value):

        self.name = name
        self.value = value

####

MAXIMA =\
{'health': 100,
 'armour': 100,
 'strength': 100}

EQUIP =\
{'health': 100,
 'armour': 0,
 'strength': 1}

####

def ut_main():

    equip = Equipment(MAXIMA, EQUIP)
    print(equip)

    print('pickup')

    armour = Gadget('armour', 42)
    print(equip.pickup(armour))
    print(equip)

    health = Gadget('health', 99)
    print(equip.pickup(health))
    print(equip)

    strength = Gadget('strength', 200)
    print(equip.pickup(strength))
    print(equip)

    print('pickup new')
    key = Gadget('key', 1)
    print(equip.pickup(key))
    print(equip)

    print('laydown')
    print(equip.laydown('health', 10))
    print(equip)

    print(equip.laydown('health', 20))
    print(equip)

    print(equip.laydown('key'))
    print(equip)

####

if __name__ == '__main__':

    ut_main()




