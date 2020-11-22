import math


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


class HP_Object:
    def __init__(self, hp: int, resistance: list):
        '''

        :param hp:  total hp of the object
        :param resistance: Is the resistance between 0 and 1 -> [EM, Therm, Kinetic, Explosive]
        '''
        self.max_hp = hp
        self.hp = hp
        self.resistance = resistance

    def modify_hp(self, amount) -> int:
        '''
        Modifies HP with either an attack or healing
        :param amount: amount to be healed by
        :return: status if the hp_object is fully_healed, depleted or damaged
        '''
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
            return status['fully_healed']
        elif self.hp > self.max_hp:
            self.hp = self.max_hp
            return status['depleted']
        else:
            return status['damaged']

    def be_attacked(self, damage: damage_types):
        for damage_type, damage_res in zip(damage.damage_component, self.resistance):
            self.modify_hp(damage_type * (1 - damage_res * 0.01))


class Shield(HP_Object):
    def __init__(self, shield_dict):
        super().__init__(shield_dict['hp'], shield_dict['resistance'])
        self.shield_leak = shield_dict['shield_leak']
        self.recharge_time = shield_dict['recharge_time']

    def recharge_tick(self) -> float:
        '''
        :return: https://wiki.eveuniversity.org/Tanking#Understand_Shield_Recharge_Rate
        '''
        shield_cap_ratio = (self.hp / self.max_hp)
        recharge_value = (10 * self.max_hp / self.recharge_time) * (math.sqrt(
            shield_cap_ratio) - shield_cap_ratio)  # https://wiki.eveuniversity.org/Tanking#Understand_Shield_Recharge_Rate
        return recharge_value


class Armor(HP_Object):
    def __init__(self, armor_dict):
        super().__init__(armor_dict['hp'],
                         armor_dict['resistance'])


class Hull(HP_Object):
    def __init__(self, hull_dict):
        super().__init__(hull_dict['hp'],
                         hull_dict['resistance'])
