import math
from typing import Tuple


class damage_types:
    def __init__(self, component_list: list):
        '''

        :param component_list: -> damage component has [EM, Therm, Kinetic, Explosive]
        '''
        self.damage_component = component_list

    def get_EM(self):
        return self.damage_component[0]

    def get_Thermal(self):
        return self.damage_component[1]

    def get_Kinetic(self):
        return self.damage_component[2]

    def get_Explosive(self):
        return self.damage_component[3]


status = {
    'fully_healed': 0,
    'depleted': -2,
    'damaged': -1
}

dict_damage_types = ["em", "therm", "kin", "exp"]


class HP_Object:

    def __init__(self, hp: int, resonance: dict):
        '''

        :param hp:  total hp of the object
        :param resistance: Is the resistance between 0 and 1 -> [EM, Therm, Kinetic, Explosive]
        '''

        self.max_hp = hp
        self.hp = hp
        self.resistance = [  # value given is resonance (1-resistance value)
            1 - resonance["em"],
            1 - resonance["therm"],
            1 - resonance["kin"],
            1 - resonance["exp"]
        ]

        self.resonance = resonance

    def modify_hp(self, amount) -> Tuple[int, int]:
        '''
        Modifies HP with either an attack or healing
        :param amount: amount to be healed by
        :return: status if the hp_object is fully_healed, depleted or damaged and remaining damage.
        '''
        self.hp -= amount
        remaining_damage = 0
        if self.hp < 0:
            remaining_damage = -1 * (self.hp - amount)
            self.hp = 0
            return status['depleted'], remaining_damage
        elif self.hp > self.max_hp:
            self.hp = self.max_hp
            return status['fully_healed'], remaining_damage
        else:
            return status['damaged'], remaining_damage

    def be_attacked(self, damage_dealt_types: dict):
        total_damage = 0
        count = 0
        for weapon in damage_dealt_types.items():
            # for damage_type, damage_res in zip(dict_damage_types, self.resistance):
            damage_type = weapon[0]
            total_damage += damage_dealt_types[damage_type] * self.resonance[damage_type]
            count += 1
        return total_damage


class Shield(HP_Object):
    def __init__(self, shield_dict: dict):
        super().__init__(shield_dict['hp']["shield"],
                         shield_dict['resonance']['shield'])
        self.shield_leak = 0.25  # shield_dict['shield_leak'] # todo: assume 0.25
        self.recharge_time = shield_dict['shieldrechargetime'] / 1000

    def recharge_tick(self) -> float:
        '''
        :return: https://wiki.eveuniversity.org/Tanking#Understand_Shield_Recharge_Rate
        '''
        shield_cap_ratio = (self.hp / self.max_hp)
        recharge_value = (10 * self.max_hp / self.recharge_time) * (math.sqrt(
            shield_cap_ratio) - shield_cap_ratio)  # https://wiki.eveuniversity.org/Tanking
        # #Understand_Shield_Recharge_Rate
        return recharge_value


class Armor(HP_Object):
    def __init__(self, armor_dict):
        super().__init__(armor_dict['hp']['armor'],
                         armor_dict['resonance']['armor'])


class Hull(HP_Object):
    def __init__(self, hull_dict):
        super().__init__(hull_dict['hp']['hull'],
                         hull_dict['resonance']['hull'])
