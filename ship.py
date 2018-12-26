#! /usr/bin/env python
import numpy as np

class location:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class ship:
    def __init__(self, hitpoints,damage,range,speed,inertia,name,x,y,z):
        self.hp = hitpoints
        self.dps = damage
        self.range = range
        self.speed = speed
        self.inertia = inertia
        self.name = name
        self.loc = location(x,y,z)
        if self.dps < 0:
            self.is_logi = True
        else:
            self.is_logi = False


    def check_range(self,target):
        x = self.loc.x - target.loc.x
        y = self.loc.y - target.loc.y
        z = self.loc.z - target.loc.z

        mag = np.array([x,y,z])
        return np.linalg.norm(mag)

    def attack(self,target):
        if self.check_range(target) <= self.range:
            target.hp -= self.dps

    def update_health(self):
        pass

    def move_to(self,target):
        x = self.loc.x - target.loc.x
        y = self.loc.y - target.loc.y
        z = self.loc.z - target.loc.z

        mag = np.array([x,y,z])
        mag = np.linalg.norm(mag)
        x *= self.speed/mag
        y *= self.speed/mag
        z *= self.speed/mag
        self.loc.x -= x
        self.loc.y -= y
        self.loc.z -= z
        print(str(self.loc.x) + " " + str(self.loc.y) + " " + str(self.loc.z))
        print("Range of ship : " + str(self.range))

    def main_attack_procedure(self,target):
        print("main_attack_procedure" + str(self.check_range(target)))
        if self.check_range(target) > self.range:
            self.move_to(target)
        else:
            self.attack(target)

ship1 = ship(50,10,10,5,1,"Thanatos",50,100,20)
ship2 = ship(50,4,50,2,1,"BoopityBoppity",50,150,20)


while ship2.hp > 0:
    ship1.main_attack_procedure(ship2)
    #ship1.attack(ship2)
    print(ship2.hp)
    if(ship2.hp <= 0):
        print(ship2.name + " destroyed")


