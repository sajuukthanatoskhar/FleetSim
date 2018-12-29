#! /usr/bin/env python
import numpy as np
import weakref
import random
import os
debug = 0

class fleet():
    fleets = []

    def __init__(self,name):
        self.__class__.fleets.append(weakref.proxy(self)) #all fleets are tracked because why not
        self.name = name
        self.ships = []
        self.is_anchor = False
        self.currentanchor = None

    def add_ship_to_fleet(self,ship):
        self.ships.append(ship)

    def remove_ship(self,ship,reason):
        for i in self.ships:
            if i.name == ship.name:
                del i


    def range_from_anchor(self,ship):
        ship.calc_distance(self.currentanchor)


    def default_fleet_activity(self):
        #attack other fleet
        #for f in
        pass


    def set_anchor(self,ship):
        for i in range(0,len(self.ships)):
            self.ships[i].is_anchor = False
        ship.is_anchor = True
        self.currentanchor = ship

    def anchorup(self,distance):
        not_everyone_anchored = False
        for i in range(0, len(FleetRed.ships)):
            if self.ships[i].is_anchor == True:
                continue
            if self.ships[i].calc_distance(self.currentanchor) > distance:
                self.ships[i].move_ship_to(self.currentanchor)
                not_everyone_anchored = True
        if not_everyone_anchored == True:
            return 0  #GODDAMN TRYRM GUYS
        else:
            return 1  #If everyone is anchored and in range - we get a return 1 and PGL is happy





    def attack_other_fleet(self,fleet,method):
        if method == "Basic Anchor and attack":
            pass
        if method == "Evasive":
            pass
        if method == "Break Anchor":
            pass #oh jesus please help me oh lawd take the wheel


        #Enemy Fleet

        #get enemy fleet distances
        #go for the shortest one
        #attack at all costs

        #distances = []

        #for enemy in fleet.ships:

        #for s in self.ships:



    def printstats(self):
        for s in self.ships:
            print("%-30s %-10s %-10d %-5d %-5d %-5d %-10s" % (s.name, self.name, s.hp, s.loc.x, s.loc.y, s.loc.z, s.is_anchor))


class location:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class ship:
    instances = []
    def __init__(self, hitpoints,damage,range,speed,inertia,name,x,y,z,fleet):
        self.hp = hitpoints
        self.dps = damage
        self.range = range
        self.speed = speed
        self.inertia = inertia
        self.name = name
        self.loc = location(x,y,z)

        if fleet != None:
            self.fleet = fleet





        if self.dps < 0:
            self.is_logi = True
        else:
            self.is_logi = False
        self.__class__.instances.append(weakref.proxy(self))


    def check_range(self,target):
        x = self.loc.x - target.loc.x
        y = self.loc.y - target.loc.y
        z = self.loc.z - target.loc.z

        mag = np.array([x,y,z])
        return np.linalg.norm(mag)

    def attack(self,target):
        if self.check_range(target) <= self.range:
            target.hp -= self.dps
        if target.hp <=0:
            print("*************%s destroyed **********************" % target.name)

    def update_health(self):
        pass


    def calculate_location_3d_diff(self,target):
        x = self.loc.x - target.loc.x
        y = self.loc.y - target.loc.y
        z = self.loc.z - target.loc.z
        return x,y,z

    def calc_distance(self,target):
        x = self.loc.x - target.loc.x
        y = self.loc.y - target.loc.y
        z = self.loc.z - target.loc.z

        return np.sqrt(x**2+y**2+z**2)
    def move_ship_to(self,target):

        x,y,z = self.calculate_location_3d_diff(target)

        mag = np.array([x,y,z])
        mag = np.linalg.norm(mag)
        if mag != 0:
            x *= self.speed/mag
            y *= self.speed/mag
            z *= self.speed/mag
            self.loc.x -= x
            self.loc.y -= y
            self.loc.z -= z
        #print(str(self.loc.x) + " " + str(self.loc.y) + " " + str(self.loc.z))
        #print("Range of " + str(self.name) + " : " + str(self.range))



    def main_attack_procedure(self,target):
        if debug == 1:
            print("Debug - main_attack_procedure\nRange of " + self.name + " to " + target.name + " :" + str(self.check_range(target)))
        if self.check_range(target) > self.range:
            self.move_ship_to(target)
        else:
            self.attack(target)

    def evasive_attack_procedure(self,target,evasiverange):
        if self.range < evasiverange:
            evasiverange = self.range
            print("Incorrect Range/Evasive Range")

        if debug == 1:
            print("Debug - Evasive Attack Procedure\nRange of " + self.name + " to " + target.name + " :" + str(self.check_range(target)) + " ~ ~ Evasive Range Set - " + str(evasiverange))
        if self.check_range(target) > self.range:
            self.move_ship_to(target)
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
    print("\n%-30s %-10s %-10s %-5s %-5s %-5s %-10s" % ("Ship Name","Fleet","Ship HP","X","Y","Z","Is Anchor"))

def printstats(ship):
    print("%-30s %-10s %-10d %-5d %-5d %-5d"% (ship.name,ship.fleet.name,ship.hp,ship.loc.x,ship.loc.y,ship.loc.z))
    # print("%s" % ship.name)
    #print(str(ship.name) + "\t\t\t" + str(ship.hp) + "\t" + str(ship.loc.x) +"\t" + str(ship.loc.y) +"\t" + str(ship.loc.z) )

FleetRed = fleet("Red")
FleetBlue = fleet("Blue")




#ship1 = ship(40,10,10,5,1,"Thanatos",50,100,20,FleetRed)
#ship2 = ship(50,9,50,2,1,"BoopityBoppity",50,150,20,FleetBlue)

#FleetRed.add_ship_to_fleet(ship1)
#FleetBlue.add_ship_to_fleet(ship2)
for i in range(0,10,1):
    FleetRed.ships.append(ship(40,10,10,5,1,"Thanatos "+str(i),random.randint(30,150),100,20,FleetRed))
    FleetBlue.ships.append(ship(50,9,50,2,1,"BoopityBoppity " +str(i),50,150,20,FleetBlue))
#while ship2.hp > 0 and ship1.hp > 0:

    #ship1.main_attack_procedure(ship2)
    #ship2.evasive_attack_procedure(ship1,30)
FleetRed.ships.append(ship(40,10,10,5,1,"Shitty Pilot #1",100,100,20,FleetRed))
FleetRed.set_anchor(FleetRed.ships[0])
while(True):
    if FleetRed.anchorup(10) == 1:
        break
    else:
        printstatsheader()
        FleetRed.printstats()
        #FleetBlue.printstats()


#anchor.findclosesthostileshipinfleet(FleetBlue)




#del FleetRed.ships[1]

#print(FleetRed.ships[1].name)




    #printstats(ship1)
    #printstats(ship2)
print("---------------------------------------------------------")
    # print("Ship 1" + str(ship1.name) + " " + str(ship1.hp))
    # print("Ship 2" + str(ship2.name) + " " + str(ship2.hp))



