import ship
import numpy as np


class turret():
    def __init__(self, optimal, falloff, dps, name,wsa,turretsig):
        self.optimal = optimal
        self.falloff = falloff
        self.dps = dps
        self.name = name

        self.turretsig = turretsig
        self.tracking = self.convert_wsa_rads(wsa)
    def convert_wsa_rads(self,wsa):
        return int(wsa)*self.turretsig/40000 #todo convert wsa to rads, but I am on a plane and can't check the formula RIP

    def fire_weapon(self):
        return self.dps


        #checktarget

        #if in range
        #return 1
        #else
        #   return 0


class missile_turret():
    pass


def parse_weapon(weapon):
    weaponfile = open(weapon, 'r')
    weaponlines = weaponfile.readlines()
    name,optimal,falloff,dps,wsa = map(str,weaponlines)
    # shipspecs.append(input("Name of Turret"))
    # shipspecs.append(input("Optimal of Turret"))
    # shipspecs.append(input("Falloff of Turret"))
    # shipspecs.append(input("DPS of Turret"))
    # shipspecs.append(input("WSA of Turret"))
    weapon = turret(int(optimal),int(falloff),int(dps),name,int(wsa),40)
    print("Weapon optimal+falloff %s + %s"%(weapon.optimal,weapon.falloff))
    weapon.tracking = weapon.convert_wsa_rads(wsa)
    return weapon

