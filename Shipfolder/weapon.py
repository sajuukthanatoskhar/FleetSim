import Shipfolder.eve_module

class Weapon(Shipfolder.eve_module.module):
    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


