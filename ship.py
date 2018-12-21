#! /usr/bin/env python



class ship:
    def __init__(self, hitpoints,damage,range,speed,inertia,name):
        self.hp = hitpoints
        self.dps = damage
        self.range = range
        self.speed = speed
        self.inertia = inertia
        self.name = name


    def attack(self,target):
        pass

    def update_health(self):
        pass

