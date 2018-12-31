import ship
import numpy as np
class turret():
    def __init__(self, optimal, falloff, dps, name,wsa):
        self.optimal = optimal
        self.falloff = falloff
        self.dps = dps
        self.name = name
        self.tracking = wsa #todo: modify and convert this to rad/s


    def fire_weapon(self):
        return self.dps


        #checktarget

        #if in range
        #return 1
        #else
        #   return 0


class missile_turret(turret):
    pass