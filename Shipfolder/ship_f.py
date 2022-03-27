#! /usr/bin/env python
import math
import random
import weakref
from typing import Tuple

import numpy as np

import Shipfolder.capacitor
import Shipfolder.ship_health
import Shipfolder.weapon
import fleet

debug = 0


class location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xold = x
        self.yold = y
        self.zold = z

    def find_distance_for_translation(self) -> float:
        """

        :return: the distance
        """
        if self.xold == None or self.yold == None or self.zold == None:
            return 0
        else:
            return math.sqrt((self.x - self.xold) ** 2 + (self.y - self.yold) ** 2 + (self.z - self.zold) ** 2)

    def translate_location(self) -> None:
        """

        :return:
        """
        self.xold = self.x
        self.yold = self.y
        self.zold = self.z


def get_type_damage(weapon: dict, avg: float) -> dict:
    """
    Gets the total type damage done
    :param weapon: The current weapon being shot with
    :param avg: the average damage modifier
    :return: dictionary of em/therm/kin/exp damage being done to the enemy ship
    """
    type_damage = {}
    for damage_type in weapon["dps_spread"].items():
        type_damage[damage_type[0]] = damage_type[1] * avg
    return type_damage


def get_spread(weapon: dict) -> dict:
    """
    Gets a dict of the em/therm/kin/exp percentage share of total volley damage
    :param weapon: The current weapon being shot with
    :return:
    """
    spread = {}
    for damage_type in weapon["dps_spread"].items():
        spread[damage_type[0]] = damage_type[1] / weapon["dps"]
    return spread


class Ship:
    instances = []

    def __init__(self, ship_dict, x=0, y=0, z=0):
        """

        :param ship_dict: just a
        :param x: starting x coordinate
        :param y: starting y coordinate
        :param z: starting z coordinate
        """
        self.ship_inf = ship_dict
        self.dps = ship_dict['weaponDPS']
        self.targettingrange = ship_dict['maxTargetRange']
        self.speed = ship_dict['maxSpeed']  # this is not the base speed if there is an afterburner present

        if ship_dict["usingMWD"] == 1:
            self.speed_MWDprop = ship_dict['mwdPropSpeed']
            self.unpropedSig = ship_dict['unpropedSig']
            self.unpropedSpeed = ship_dict['unpropedSpeed']

        try:
            self.inertia = ship_dict['inertia']
        except KeyError:
            print("Key error- No inertia entry - setting to 1.5")
            self.inertia = 1.5
        self.name = "".join(filter(str.isalnum, ship_dict['name']))
        self.loc = location(x,
                            y,
                            z)

        self.projection = ship_dict['projections']
        self.signature = ship_dict['signatureRadius']
        self.can_lock = True
        self.jammed_by = []
        self.marker = 'o'
        # Health and Capacitor
        self.ship_shield = Shipfolder.ship_health.Shield(ship_dict)
        self.ship_armor = Shipfolder.ship_health.Armor(ship_dict)
        self.ship_hull = Shipfolder.ship_health.Hull(ship_dict)
        self.ship_capacitor = Shipfolder.capacitor.capacitor(ship_dict)
        self.hp = [self.ship_shield.hp, self.ship_armor.hp, self.ship_hull.hp]
        # Fleet Sim Related
        self.current_target = None
        self.damage_dealt_this_tick = None
        self.distance_from_target = None
        self.drone_bay = None
        self.angular_velocity = None  # angular velocity of current target

        if fleet != None:
            self.fleet = fleet

        if self.dps < 0:
            self.is_logi = True
        else:
            self.is_logi = False

        self.weapon = ship_dict['weapons']  # todo: problem here

        self.weapons = [Shipfolder.weapon.Weapon(a_weapon) for a_weapon in ship_dict['weapons']]
        self.loss_mail_final_blow_ship = {}  # A ship will be on here
        self.loss_mail_damage_lost = {}
        self.__class__.instances.append(weakref.proxy(self))

    def check_range(self, target: location):
        x = self.loc.x - target.x
        y = self.loc.y - target.y
        z = self.loc.z - target.z

        mag = np.array([x, y, z])
        return round(np.linalg.norm(mag))

    def attack(self, target: Shipfolder):
        """
        Checks that
        :param target:
        :return:
        """

        # todo: requires test

        self.damage_dealt_this_tick = 0
        if not self.sensor_check(target):  # check if we are able to lock the target (sensor damps and ecm)
            return 0

        for weapon in self.weapon:  # go through all weapon systems
            if self.weapon_is_cycling(weapon):  # todo: weapon cycling requires a second tick system
                return 0
            success_value, test_value = self.calc_weapon_to_hit_chance(weapon, target)
            if test_value > success_value:  # Weapon miss
                self.damage_dealt_this_tick = 0
                return 0

            spread = get_spread(weapon)  # check the fractional %tage of damage
            still_damaging = True
            avg = self.calc_weapon_mod(test_value)  # use test value to indicate damage modifier
            damage_dealt = get_type_damage(weapon, avg)

            while still_damaging:
                """
                Recursively deal damage to the ship until we run out of damage to process on shield/armor/hull or
                the ship is dead
                """
                damage_this_round, damage_dealt, still_damaging = self.deal_damage(spread, weapon, damage_dealt, target,
                                                                                   still_damaging)
                self.damage_dealt_this_tick += damage_this_round

        if target.ship_hull.hp <= 0:
            target.hp = 0
            print("*************%s destroyed **********************" % target)

    def calculate_location_3d_diff(self, target: location) -> tuple:
        """

        :param target:
        :return:
        """
        x = self.loc.x - target.x
        y = self.loc.y - target.y
        z = self.loc.z - target.z
        return x, y, z

    def calc_distance(self, target: location) -> float:
        """

        :param target:
        :return:
        """
        x = self.loc.x - target.x
        y = self.loc.y - target.y
        z = self.loc.z - target.z

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
            try:
                sum = (a ** 2 - b ** 2 - c ** 2) / (-2 * b * c)
            except ZeroDivisionError:
                print("At 0m")
                sum = 0
                #todo: wrong, but its better than nothing

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

    def calc_weapon_mod(self, chance):
        """
        Modifies weapon damage
        :param chance:
        :return:
        """
        if chance >= 0.01:
            return chance + 0.49
        else:
            return 3

        # mod = 1 - chance
        # lower = 0.5
        # upper = 1.49 - mod
        # # lower, upper, avgdps = self.calc_weapon_mod(target)
        # avgdps = (chance - 0.01) * ((lower + upper) / 2) + 0.03
        # return lower, upper, avgdps

    def calc_weapon_to_hit_chance(self, weapon: dict, target: Shipfolder):
        chance = 0.5 ** ((self.calculate_angular(target) / (weapon["tracking"] * target.signature) ** 2 + (
                max(0, (self.calc_distance(target.loc) - weapon["optimal"])) / weapon["falloff"]) ** 2))
        # chance = 0.5
        testedvalue = random.random()
        return chance, testedvalue

    def move_ship_to(self, target_location_point: location) -> None:
        """
        Moves ship to an area
        :param target_location_point:
        :return:
        """
        try:
            vect_x, vect_y, vect_z = self.calculate_location_3d_diff(target_location_point)
        except AttributeError as e:
            print("{} : should be ship.location but is {}\nzeroing vectors".format(e, type(target_location_point)))
            vect_x, vect_y, vect_z = 0

        mag = np.array([vect_x, vect_y, vect_z])
        mag = np.linalg.norm(mag)
        if mag != 0:
            self.move(mag, vect_x, vect_y, vect_z)

    def move(self, mag, x, y, z):
        """
        Physically translates the ship to move to the point
        :param mag:
        :param x:
        :param y:
        :param z:
        :return:
        """
        x *= self.speed / mag
        y *= self.speed / mag
        z *= self.speed / mag
        self.loc.translate_location()
        self.loc.x -= x
        self.loc.y -= y
        self.loc.z -= z

    def orbit_around_target(self, target: Shipfolder, distance: int) -> None:
        """
        Gets ship to orbit aroudn target
        :param target:
        :param distance:
        :return:
        """
        x, y, z = self.calculate_location_3d_diff(target.loc)
        mag = np.array([x, y, z])
        mag = np.linalg.norm(mag)
        if mag > distance:
            self.move(mag, x, y, z)
        else:  # Orbit
            orbit_points: list[location] = self.create_orbit_points(target, orbitrange=distance)  # Set up orbit points
            closestpoint = {"point_no": None, "point_dist": None}
            for point in orbit_points:
                pointx = self.loc.x - point.x
                pointy = self.loc.y - point.y
                pointz = self.loc.z - point.z
                mag = np.array([pointx, pointy, pointz])
                mag = np.linalg.norm(mag)

                if not closestpoint['point_no'] and not closestpoint['point_dist']:
                    # for the first point
                    closestpoint['point_no'] = point
                    closestpoint['point_dist'] = mag
                else:  # Find closest point
                    if closestpoint['point_dist'] > mag:
                        closestpoint['point_no'] = point
                        closestpoint['point_dist'] = mag

            pointx, pointy, pointz = self.calculate_location_3d_diff(closestpoint['point_no'])
            mag = np.array([pointx, pointy, pointz])
            mag = np.linalg.norm(mag)

            if mag > distance:
                self.move(mag, x, y, z)

    def keep_at_range(self, target: Shipfolder, distance) -> None:
        """

        :param target:
        :param distance:
        :return:
        """
        x, y, z = self.calculate_location_3d_diff(target.loc)
        mag = np.array([x, y, z])
        mag = np.linalg.norm(mag)

        if mag > distance:
            self.move(mag, x, y, z)
        else:
            pass
            # Move

    def main_attack_procedure(self, target):
        self.distance_from_target = self.check_range(target.loc)
        if debug == 1:
            print("Debug - main_attack_procedure\nRange of " + self.name + " to " + target.name + " :" + str(
                self.check_range(target.loc)))
        if self.check_range(target.loc) > self.targettingrange:
            print(
                "Target Distance %s, ship target range %s" % (
                str(self.check_range(target.loc)), str(self.targettingrange)))

            # No, there is no movement, this is strictly an attack protocol.  Wtf, who coded this?  Oh it was me, Sajuuk
            self.damage_dealt_this_tick = 0
            pass
        else:
            self.attack(target)

    def evasive_attack_procedure(self, target: Shipfolder, evasiverange):
        self.distance_from_target = self.check_range(target.loc)
        if self.targettingrange < evasiverange:
            evasiverange = self.targettingrange
            print("Incorrect Range/Evasive Range")

        if debug == 1:
            print("Debug - Evasive Attack Procedure\nRange of " + self.name + " to " + target.name + " :" + str(
                self.check_range(target.loc)) + " ~ ~ Evasive Range Set - " + str(evasiverange))
        if self.check_range(target.loc) > self.targettingrange:
            self.move_ship_to(target.loc)
        elif self.check_range(target.loc) < evasiverange:
            self.move_away_from(target)
        else:
            self.attack(target)

    def move_away_from(self, target):
        """
        Gets the ship to move away from a target
        todo: should be a point in space
        :param target:
        :return:
        """
        x, y, z = self.calculate_location_3d_diff(target)
        mag = np.array([x, y, z])
        mag = np.linalg.norm(mag)
        x *= self.speed * -1 / mag
        y *= self.speed * -1 / mag
        z *= self.speed * -1 / mag
        self.loc.x -= x
        self.loc.y -= y
        self.loc.z -= z

    def sensor_check(self, target: Shipfolder):
        """
        Checks that the target is in range
        :param target: The ship that is being locked
        :return: 0 for no lock possible, 1 for lock possible on target
        """
        if self.check_range(target.loc) <= self.targettingrange and \
                ((not self.can_lock and self.target_is_jammer(target.loc)) or self.can_lock):
            return 1
        else:
            self.damage_dealt_this_tick = 0
            return 0

    def target_is_jammer(self, target):
        """
        Checks that the target is an ecm jammer
        :param target: a ship that is jamming this current ship
        :return:
        """
        return target in self.jammed_by

    def weapon_is_cycling(self, weapon: dict) -> bool:
        pass
        if (weapon):
            return False
        else:
            return True  # todo: to factor in weapon cycle times, at the moment

    def deal_damage(self, spread: dict, weapon: dict,
                    damage_dealt: dict, target: Shipfolder, still_damaging: bool) -> Tuple[float, dict, bool]:
        status = None
        raw_hp_damage = 0
        remaining_damage = 0
        for hp_component in [target.ship_shield, target.ship_armor, target.ship_hull]:
            if hp_component.hp <= 0:
                continue  # move to next component to be damaged
            raw_hp_damage = hp_component.be_attacked(damage_dealt)
            status, remaining_damage = hp_component.modify_hp(raw_hp_damage)
            break
        try:
            if target.ship_hull.hp <= 0 or remaining_damage <= 0:
                still_damaging = False
        except Exception as e:
            print(e)
        if target.ship_hull.hp > 0:
            damage_dealt = self.split_back_to_components(spread, weapon, remaining_damage)

        return raw_hp_damage - remaining_damage, damage_dealt, still_damaging

    def split_back_to_components(self, spread: dict, weapon: dict, remaining_damage: float) -> dict:
        """
        Splits the remaining damage back to type damage
        :param spread: the percentage of spread
        :param weapon: The weapon being used
        :param remaining_damage: The remaining damage after piercing shield or armor
        :return:
        """
        damage_split_dict = {}
        for damage_type in weapon["dps_spread"].items():
            damage_split_dict[damage_type[0]] = spread[damage_type[0]] * remaining_damage

        return damage_split_dict

    def create_orbit_points(self, target, orbitrange=5000, points=8, inclination=0) -> [location]:
        import math
        orbit_points = []

        for point_number in range(0, points):
            orbit_points.append(location(orbitrange * math.cos(point_number * (math.pi * 2 / points)) + target.loc.x,
                                         orbitrange * math.sin(point_number * (math.pi * 2 / points)) + target.loc.y,
                                         orbitrange * 0 + target.loc.z))

        return orbit_points


def printstatsheader():
    # print("%30s %s\t%s\t%\t%s"%("Shipfolder Name","Shipfolder HP","X","Y","Z"))
    print("\n%-30s %-10s %-10s %-5s %-5s %-5s %-10s %-25s %-20s %-15s %-25s" % (
        "Shipfolder Name", "Fleet", "Shipfolder HP", "X", "Y", "Z", "Is Anchor", "Target", "Distance", "Damage Dealt",
        "Angular Velocity"))
    return ("\n%-30s %-10s %-10s %-5s %-5s %-5s %-10s %-25s %-20s %-15s %-25s" % (
        "Shipfolder Name", "Fleet", "Shipfolder HP", "X", "Y", "Z", "Is Anchor", "Target", "Distance", "Damage Dealt",
        "Angular Velocity"))
