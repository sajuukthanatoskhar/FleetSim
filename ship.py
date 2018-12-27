#! /usr/bin/env python
import numpy as np

debug = 0

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


    def calculate_location_3d_diff(self,target):
        x = self.loc.x - target.loc.x
        y = self.loc.y - target.loc.y
        z = self.loc.z - target.loc.z
        return x,y,z


    def move_to(self,target):

        x,y,z = self.calculate_location_3d_diff(target)

        mag = np.array([x,y,z])
        mag = np.linalg.norm(mag)
        x *= self.speed/mag
        y *= self.speed/mag
        z *= self.speed/mag
        self.loc.x -= x
        self.loc.y -= y
        self.loc.z -= z
        print(str(self.loc.x) + " " + str(self.loc.y) + " " + str(self.loc.z))
        print("Range of " + str(self.name) + " : " + str(self.range))

    def main_attack_procedure(self,target):
        if debug == 1:
            print("Debug - main_attack_procedure\nRange of " + self.name + " to " + target.name + " :" + str(self.check_range(target)))
        if self.check_range(target) > self.range:
            self.move_to(target)
        else:
            self.attack(target)

    def evasive_attack_procedure(self,target,evasiverange):
        if self.range < evasiverange:
            evasiverange = self.range
            print("Incorrect Range/Evasive Range")

        if debug == 1:
            print("Debug - Evasive Attack Procedure\nRange of " + self.name + " to " + target.name + " :" + str(self.check_range(target)) + " ~ ~ Evasive Range Set - " + str(evasiverange))
        if self.check_range(target) > self.range:
            self.move_to(target)
        elif self.check_range(target) < evasiverange:
            self.move_away_from(target)
        else:
            self.attack(target)

    def move_away_from(self,target):
        x,y,z = self.calculate_location_3d_diff(target)
        mag = np.array([x,y,z])
        mag = np.linalg.norm(mag)
        x *= self.speed*-1/mag
        y *= self.speed*-1/mag
        z *= self.speed*-1/mag
        self.loc.x -= x
        self.loc.y -= y
        self.loc.z -= z

def printstatsheader():
    #print("%30s %s\t%s\t%\t%s"%("Ship Name","Ship HP","X","Y","Z"))
    print("%-30s %-10s %-5s %-5s %-5s" % ("Ship Name","Ship HP","X","Y","Z"))

def printstats(ship):
    print("%-30s %-10d %-5d %-5d %-5d"% (ship.name,ship.hp,ship.loc.x,ship.loc.y,ship.loc.z))
    # print("%s" % ship.name)
    #print(str(ship.name) + "\t\t\t" + str(ship.hp) + "\t" + str(ship.loc.x) +"\t" + str(ship.loc.y) +"\t" + str(ship.loc.z) )


ship1 = ship(40,10,10,5,1,"Thanatos",50,100,20)
ship2 = ship(50,9,50,2,1,"BoopityBoppity",50,150,20)


while ship2.hp > 0 and ship1.hp > 0:

    ship1.main_attack_procedure(ship2)
    ship2.evasive_attack_procedure(ship1,30)
    printstatsheader()
    printstats(ship1)
    printstats(ship2)
    print("---------------------------------------------------------")
    # print("Ship 1" + str(ship1.name) + " " + str(ship1.hp))
    # print("Ship 2" + str(ship2.name) + " " + str(ship2.hp))
    if(ship2.hp <= 0):
        print(ship2.name + " destroyed")
    if(ship1.hp <= 0):
        print(ship1.name + " destroyed")


