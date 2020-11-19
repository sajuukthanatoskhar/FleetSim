import math
from Ship.ship_health import status

class capacitor:
    def __init__(self, capacitor_capacity, time_to_recharge, neut_resistance: float):
        self.capacitor_level = capacitor_capacity
        self.max_capacitor = capacitor_capacity
        self.recharge_time = time_to_recharge
        if neut_resistance > 1:
            raise Exception("Energy Neutralizer must be between 0 and 1 in decimal")
        else:
            self.neut_res = neut_resistance

    def recharge_tick(self):
        capacitor_cap_ratio = (self.capacitor_level / self.max_capacitor)
        recharge_value = (10 * self.max_capacitor / self.recharge_time) * (math.sqrt(capacitor_cap_ratio) - capacitor_cap_ratio)  # https://wiki.eveuniversity.org/Tanking#Understand_Shield_Recharge_Rate
        return recharge_value

    def modify_capacitor(self, amount, rep = False) -> (int, float):
        '''
        Modifies HP with either an attack or healing
        :param rep: is it a repairer or not
        :param amount: amount to be healed by
        :return: status if the hp_object is fully_healed, depleted or damaged
        '''
        reflected = 0
        if rep is True:
            reflected = self.capacitor_damage(-1*amount)
        else:
            self.capacitor_level -= self.capacitor_damage(amount)[0]
        if self.capacitor_level < 0:
            self.capacitor_level = 0
            return status['depleted'], 0
        elif self.capacitor_level > self.max_capacitor:
            self.capacitor_level = self.max_capacitor
            return status['fully_healed'], reflected
        else:
            return status['damaged'], reflected

    def capacitor_damage(self, damage: int) -> (float, float):
        """

        :param damage: incoming damage to the capacitor (Not permanent!) :)
        :return: the amount that it was damaged by
        """
        if damage > 0:
            cap_damage = damage * (1-self.neut_res)
            self.capacitor_level -= cap_damage
            reflected_cap_damage = damage * self.neut_res
            return cap_damage, reflected_cap_damage
        else:
            self.capacitor_level -= damage
            return damage, 0