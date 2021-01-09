#! /usr/bin/env python
import json
import sys
import UDP_Server_Client.Server_Client
import fleet
import numpy as np
import weakref
import random
import os
import pickle
import proc as proc
import Pyro4
import weaponsystems
import math
from time import sleep
import Ship.capacitor
import Ship.ship_health

debug = 0
import socket


@Pyro4.expose
class location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xold = None
        self.yold = None
        self.zold = None

    def find_distance_for_translation(self):
        if self.xold == None or self.yold == None or self.zold == None:
            return 0
        else:
            return math.sqrt((self.x - self.xold) ** 2 + (self.y - self.yold) ** 2 + (self.z - self.zold) ** 2)

    def translate_location(self):
        self.xold = self.x
        self.yold = self.y
        self.zold = self.z


@Pyro4.expose
class ship:
    instances = []

    def __init__(self, ship_dict):
        self.hp = ship_dict['hitpoints']
        self.dps = ship_dict['damage']
        self.targettingrange = ship_dict['targettingrange']
        self.speed = ship_dict['speed']
        self.inertia = ship_dict['inertia']
        self.name = ship_dict['name']
        self.loc = location(ship_dict['x'],
                            ship_dict['y'],
                            ship_dict['z'])
        self.weapon = ship_dict['weapons'] # todo: problem here
        self.projection = ship_dict['projections']
        self.signature = ship_dict['signature']
        self.current_target = None
        self.damagedealt_this_tick = None
        self.distance_from_target = None
        self.drone_bay = None
        self.angular_velocity = None  # angular velocity of current target
        self.ship_shield = Ship.ship_health.Shield(ship_dict['shield'])
        self.ship_armor = Ship.ship_health.Armor(ship_dict['armor'])
        self.ship_hull = Ship.ship_health.Hull(ship_dict['hull'])
        self.ship_capacitor = Ship.capacitor.capacitor(ship_dict['capacitor'])
        if fleet != None:
            self.fleet = fleet

        if self.dps < 0:
            self.is_logi = True
        else:
            self.is_logi = False
        self.__class__.instances.append(weakref.proxy(self))


    def check_range(self, target):
        x = self.loc.x - target.loc.x
        y = self.loc.y - target.loc.y
        z = self.loc.z - target.loc.z

        mag = np.array([x, y, z])
        return np.linalg.norm(mag)

    def attack(self, target):
        success_value, test_value = self.calc_weapon_to_hit_chance(target)

        if test_value > success_value:
            self.damagedealt_this_tick = 0
            # Weapon miss
            return 0
        if self.check_range(
                target) <= self.targettingrange:  # todo: the self.range should be refactored as the targetting range AND NOT worded as if it is a turret range and falloff, that is simply wrong
            lower, upper, avg = self.calc_weapon_avg_dps_mod(target, test_value)
            target.hp -= self.weapon.dps * avg  # todo: the dps should not sit at this average - it needs to modified based on the number received from the tohit
            print("\nDPS - %d from %s " % (math.floor(self.weapon.dps * avg), self.name))
            self.damagedealt_this_tick = math.floor(self.weapon.dps * avg)

        if target.hp <= 0:
            print("*************%s destroyed **********************" % target)

    def calculate_location_3d_diff(self, target):
        x = self.loc.x - target.loc.x
        y = self.loc.y - target.loc.y
        z = self.loc.z - target.loc.z
        return x, y, z

    def calc_distance(self, target):
        x = self.loc.x - target.loc.x
        y = self.loc.y - target.loc.y
        z = self.loc.z - target.loc.z

        return np.sqrt(x ** 2 + y ** 2 + z ** 2)

    # todo: This function needs to check things.
    # todo: Remember the radial velocity function.  d
    def calculate_angular(self, target):
        if (target.loc.xold == None and target.loc.yold == None and target.loc.zold == None):
            return 1
        else:
            #            target.loc.x - target

            # calculate distance to old position -> c
            c = self.calc_dist_using_xyz(target.loc.x, target.loc.y, target.loc.z)
            # calculate distance to new position -> b
            b = self.calc_dist_using_xyz(target.loc.xold, target.loc.yold, target.loc.zold)
            # find distance between old and new positions -> a
            a = target.loc.find_distance_for_translation()
            # Use cosine rule to find solution to angle A
            # Cosine rule is used and is the following equation a**2 = b**2 + c**2 -2bc

            sum = (a ** 2 - b ** 2 - c ** 2) / (-2 * b * c)

            if sum > 1 and sum < 1.1:
                sum = 1
            if sum < -1 and sum > -1.1:
                sum = -1
            self.angular_velocity = math.acos(sum)
            return math.acos(sum)
        # math.asin will put it in terms of rads  # warning, please check if the concept is sound - yes it is
        # todo:write test case for this function please using standard triangle - i dont know if its any good or not
        # note: cosine rule is compatible with right angle triangles

        return 1

    def calc_dist_using_xyz(self, x, y, z):
        x = self.loc.x - x
        y = self.loc.y - y
        z = self.loc.z - z

        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def calc_weapon_avg_dps_mod(self, target, chance):
        # chance,testedvalue = self.calc_weapon_to_hit_chance(target)
        mod = 1 - chance
        lower = 0.5
        upper = 1.49 - mod
        # lower, upper, avgdps = self.calc_weapon_avg_dps_mod(target)
        avgdps = (chance - 0.01) * ((lower + upper) / 2) + 0.03
        return lower, upper, avgdps

    def calc_tracking_score(self):
        return self.weapon.tracking

    def calc_weapon_to_hit_chance(self, target):
        chance = 0.5 ** ((self.calculate_angular(target) / (self.calc_tracking_score() * target.signature) ** 2 + (
                    max(0, (self.calc_distance(target) - self.weapon.optimal)) / self.weapon.falloff) ** 2))
        # chance = 0.5
        testedvalue = random.random()
        return chance, testedvalue

    def move_ship_to(self, target):
        x, y, z = self.calculate_location_3d_diff(target)
        mag = np.array([x, y, z])
        mag = np.linalg.norm(mag)
        if mag != 0:
            x *= self.speed / mag
            y *= self.speed / mag
            z *= self.speed / mag
            self.loc.translate_location()
            self.loc.x -= x
            self.loc.y -= y
            self.loc.z -= z
        # print(str(self.loc.x) + " " + str(self.loc.y) + " " + str(self.loc.z))
        # print("Range of " + str(self.name) + " : " + str(self.range))

    def main_attack_procedure(self, target):
        self.distance_from_target = self.check_range(target)
        if debug == 1:
            print("Debug - main_attack_procedure\nRange of " + self.name + " to " + target.name + " :" + str(
                self.check_range(target)))
        if self.check_range(target) > self.targettingrange:
            print(
                "Target Distance %s, ship target range %s" % (str(self.check_range(target)), str(self.targettingrange)))
            # fleet.currentanchor.move_ship_to(target) #todo: is this ok?  Like what is going on here.  Is the anchor actually moving #[number of fleetmembers]# times
            # No, there is no movement, this is strictly an attack protocol.  Wtf, who coded this?  Oh it was me, Sajuuk
            self.damagedealt_this_tick = 0
            pass
        else:
            self.attack(target)

    def evasive_attack_procedure(self, target, evasiverange):
        self.distance_from_target = self.check_range(target)
        if self.targettingrange < evasiverange:
            evasiverange = self.targettingrange
            print("Incorrect Range/Evasive Range")

        if debug == 1:
            print("Debug - Evasive Attack Procedure\nRange of " + self.name + " to " + target.name + " :" + str(
                self.check_range(target)) + " ~ ~ Evasive Range Set - " + str(evasiverange))
        if self.check_range(target) > self.targettingrange:
            self.move_ship_to(target)
        elif self.check_range(target) < evasiverange:
            self.move_away_from(target)
        else:
            self.attack(target)

    def move_away_from(self, target):
        x, y, z = self.calculate_location_3d_diff(target)
        mag = np.array([x, y, z])
        mag = np.linalg.norm(mag)
        x *= self.speed * -1 / mag
        y *= self.speed * -1 / mag
        z *= self.speed * -1 / mag
        self.loc.x -= x
        self.loc.y -= y
        self.loc.z -= z


def printstatsheader():
    # print("%30s %s\t%s\t%\t%s"%("Ship Name","Ship HP","X","Y","Z"))
    print("\n%-30s %-10s %-10s %-5s %-5s %-5s %-10s %-25s %-20s %-15s %-25s" % (
    "Ship Name", "Fleet", "Ship HP", "X", "Y", "Z", "Is Anchor", "Target", "Distance", "Damage Dealt",
    "Angular Velocity"))
    return ("\n%-30s %-10s %-10s %-5s %-5s %-5s %-10s %-25s %-20s %-15s %-25s" % (
    "Ship Name", "Fleet", "Ship HP", "X", "Y", "Z", "Is Anchor", "Target", "Distance", "Damage Dealt",
    "Angular Velocity"))


if __name__ == "__main__":
    UDP_port_no = 6789
    Sender_Port_No = 6790
    UDP_IP_Address = "127.0.0.1"
    small_autocannon = weaponsystems.turret(100, 80, 90, "Small Autocannon", 8)
    FleetRed = fleet.Fleet("Red")
    FleetBlue = fleet.Fleet("Blue")
    serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversock.bind(("", UDP_port_no))
    remoteip = "192.168.178.22"
    listenersock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ship1 = ship(40,10,10,5,1,"Thanatos",50,100,20,FleetRed)
    # ship2 = ship(50,9,50,2,1,"BoopityBoppity",50,150,20,FleetBlue)

    # FleetRed.add_ship_to_fleet(ship1)
    # FleetBlue.add_ship_to_fleet(ship2)
    # for i in range(0, 10, 1):
    #     FleetRed.ships.append(
 #           ship(800, 2, 60, 5, 1, "Thanatos_" + str(i), random.randint(30, 150), random.randint(30, 150), 20, FleetRed,
  #               small_autocannon))
#        FleetBlue.ships.append(ship(500, 2, 70, 2, 1, "Nyx_" + str(i), 50, 150, 20, FleetBlue, small_autocannon))
    # while ship2.hp > 0 and ship1.hp > 0:

    # ship1.main_attack_procedure(ship2)
    # ship2.evasive_attack_procedure(ship1,30)
#    FleetRed.ships.append(ship(40, 10, 10, 5, 1, "Shitty Pilot #1", 100, 100, 20, FleetRed, small_autocannon))
#     FleetRed.choosenewanchor()
#     FleetBlue.choosenewanchor()
#     FleetRed.fleet_choose_primary_now(FleetBlue, "closest")
#     FleetBlue.fleet_choose_primary_now(FleetRed, "closest")
#     fleets = [FleetRed, FleetBlue]
    while (len(FleetRed.ships) > 0 and len(FleetBlue.ships) > 0):
        FleetRed.anchorup()
        FleetBlue.anchorup()

        # Attack
        FleetRed.attack_other_fleet(FleetBlue, "Basic Anchor and attack")
        FleetBlue.attack_other_fleet(FleetRed, "Basic Anchor and attack")

        processing_dead = 1
        #todo:
        '''
        for fleet in fleets:
            
        
        '''

        while (processing_dead):
            processing_dead = FleetRed.checkenemyfleetdead(FleetBlue)

        processing_dead = 1
        while (processing_dead):
            processing_dead = FleetBlue.checkenemyfleetdead(FleetRed)

        line = printstatsheader()
        listenersock.sendto(line.encode('UTF-8'), (remoteip, Sender_Port_No))
        # listenersock.sendto(FleetRed.printstats(),(UDP_IP_Address,Sender_Port_No))
        listy = FleetRed.printstats()
        for i in range(0, len(listy)):
            listenersock.sendto(listy[i].encode('UTF-8'), (remoteip, Sender_Port_No))

        FleetBlue.printstats()

        print("End of round")

        state = "wait-state"
        while (state == "wait-state"):
            if (UDP_Server_Client.Server_Client.send_packet(listenersock,
                                                            state, remoteip, Sender_Port_No) == -1):
                print("Error")
            else:
                state = "packet_in"

        while (state == "packet_in"):  # receiving from menu

            state = UDP_Server_Client.Server_Client.receive_packet(serversock).split(" ")

            if (state != '3'):
                print(state)
            if state == '4':
                print("Moving on")
                break
            if state[0] == '5':
                # UDP_Server_Client.Server_Client.send_packet(listenersock,state,UDP_IP_Address,Sender_Port_No)
                X = state[1]
                Y = state[2]
                Z = state[3]
                fleetname = state[4]

                print("Move to certain location - for anchor \nX = something \nY = something \nZ = something")

                break
            if state == '1':
                print("")

    # anchor.findclosesthostileshipinfleet(FleetBlue)

    # del FleetRed.ships[1]

    # print(FleetRed.ships[1].name)

    # printstats(ship1)
    # printstats(ship2)
    print("---------------------------------------------------------")
    # print("Ship 1" + str(ship1.name) + " " + str(ship1.hp))
    # print("Ship 2" + str(ship2.name) + " " + str(ship2.hp))
