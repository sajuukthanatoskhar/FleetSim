import ship
import numpy as np
class turret():
    def __init__(self, optimal, falloff, dps, name,wsa):
        self.optimal = optimal
        self.falloff = falloff
        self.dps = dps
        self.name = name
        self.tracking = self.convert_wsa_rads(wsa)

    def convert_wsa_rads(self,wsa):
        return wsa #todo convert wsa to rads, but I am on a plane and can't check the formula RIP

    def fire_weapon(self):
        return self.dps


        #checktarget

        #if in range
        #return 1
        #else
        #   return 0


class missile_turret():
    pass