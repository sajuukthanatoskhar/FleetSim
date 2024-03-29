import weakref
import Shipfolder.ship_f as ship
import Pyro4


@Pyro4.expose
class Fleet:
    fleets = []

    def __init__(self, name: str):
        self.__class__.fleets.append(weakref.proxy(self))  # all fleets are tracked because why not
        self.name = name
        self.ships = []
        self.is_anchor = False
        self.currentanchor : ship = None
        self.currenttargetstatus = -1  # -1 Not set, 0 is dead, 1 is alive
        self.currentprimary : ship = None

        self.color = 'r'
        z = 0
        y = 0
        z = 0
        self.anchor_goto_loc = ship.location(0, 0, 0)
        self.engagementrange = None
        self.anchordistance = 2000  # place holder value todo: anchordistance range should be settable by user
        self.fleet_capitulation_status = 0
        self.engagementrange = 7500  # place holder value todo: engagement range should be settable by user

    # def __init__(self,name,engagementdistance):
    #     self.__class__.fleets.append(weakref.proxy(self)) #all fleets are tracked because why not
    #     self.name = name
    #     self.ships = []
    #     self.is_anchor = False
    #     self.currentanchor = None
    #     self.currenttargetstatus = -1  #-1 Not set, 0 is dead, 1 is alive
    #     self.currentprimary = None
    #     z = 0
    #     y = 0
    #     z = 0
    #     self.anchor_goto_loc = location(0,0,0)
    #     self.engagementrange = engagementdistance
    #     self.anchordistance = 0

    def add_ship_to_fleet(self, ship):
        self.ships.append(ship)

    def remove_ship(self, ship, reason):
        for ship in self.ships:
            if ship.name == ship.name:
                self.ships.remove(ship)

    def listallfleetmembers(self):
        fleetmembers = ""
        count = 0
        for i in self.ships:
            fleetmembers += "%s %s %s %s %s %s\n"(str(count), str(i.name), str(i.hp), str(i.loc.x), str(i.loc.y),
                                                  str(i.loc.z))
        return fleetmembers

    def range_from_anchor(self, ship):
        ship.calc_distance(self.currentanchor.loc)

    def default_fleet_activity(self):
        # attack other fleet
        # for f in
        pass

    def set_anchor(self, ship):
        for i in range(0, len(self.ships)):
            self.ships[i].is_anchor = False
        ship.is_anchor = True
        self.currentanchor = ship

    def anchor_move_to_target(self, target):
        pass

    def anchorup(self):
        not_everyone_anchored = False
        for i in range(0, len(self.ships)):
            if self.ships[i].is_anchor == True:
                if self.currentprimary == None:
                    print("No Primary selected!")
                elif self.currentanchor.check_range(self.currentprimary.loc) > self.engagementrange:
                    self.currentanchor.move_ship_to(self.currentprimary.loc)
                continue
            if self.ships[i].calc_distance(self.currentanchor.loc) > self.anchordistance:  # distance should be 5000
                self.ships[i].move_ship_to(self.currentanchor.loc)
                if self.ships[i].calc_distance(self.currentanchor.loc) > self.anchordistance:
                    not_everyone_anchored = True # What should this do?  #todo:
            else:
                pass # ships should be orbiting around anchor?


        if not_everyone_anchored == True:
            return 0  # GODDAMN TRYRM GUYS
        else:
            return 1  # If everyone is anchored and in range - we get a return 1 and PGL is happy

    def chooseprimary(self, fleet, method):
        distances = []
        for ship in range(0, len(fleet.ships)):
            distances.append(self.currentanchor.calc_distance(fleet.ships[ship].loc))
        return fleet.ships[ship.np.argmin(distances)]

    def fleet_choose_primary_now(self, fleet, method):
        distances = []
        for ship in range(0, len(fleet.ships)):
            distances.append(self.currentanchor.calc_distance(fleet.ships[ship]).loc)
        self.currentprimary = fleet.ships[ship.np.argmin(distances)]

    def fleet_attack_procedure(self, target):  # based off the ship class
        if ship.debug == 1:
            print("Debug - main_attack_procedure\nRange of " + self.name + " to " + target.name + " :" + str(
                self.check_range(target)))
        if self.check_range(target) > self.range:
            self.currentanchor.move_ship_to(target.loc)
        else:
            self.attack(target)

    def attack_primary(self):
        """
        All ships in the fleet attack their target
        :return:
        """
        for ship in self.ships:
            ship.current_target = self.currentprimary
            ship.main_attack_procedure(self.currentprimary)
        if self.currentprimary.ship_hull.hp <= 0:
            self.currentprimary = None

    def attack_other_fleet(self, fleet, method):
        """
        Not Implemented any where
        todo: use callable to set not fleet, but ship behaviour, include manual/none
        :param fleet:
        :param method:
        :return:
        """
        if method == "Basic Anchor and attack":

            if (self.currenttargetstatus != 1):  # If our ship is not alive
                self.currentprimary = self.chooseprimary(fleet, "closest")

            if self.currentprimary.hp > 0:
                self.currenttargetstatus = 1
                # attack if in range
                for i in range(0, len(self.ships)):
                    self.ships[i].current_target = self.currentprimary
                    self.ships[i].main_attack_procedure(self.currentprimary, self)

            elif self.currentprimary.hp <= 0:
                self.currenttargetstatus = 0

        if method == "Evasive":
            pass
        if method == "Break Anchor":
            pass

        # Enemy Fleet

        # get enemy fleet distances
        # go for the shortest one
        # attack at all costs

        # distances = []

        # for enemy in fleet.ships:

        # for s in self.ships:

    def choosenewanchor(self):
        """
        Chooses a new anchor for the fleet
        :return:
        """
        hp = []
        for i in range(0, len(self.ships)):
            hp.append(self.ships[i].hp)
        self.set_anchor(self.ships[ship.np.argmax(hp)])
        # return fleet.ships[np.argmin(distances)]

    def checkenemyfleetdead(self, fleet):
        for i in range(0, len(fleet.ships)):
            if fleet.ships[i].ship_hull.hp <= 0:
                if fleet.currentanchor == fleet.ships[i]:
                    fleet.choosenewanchor()
                print("%s Ship Destroyed" % str(fleet.ships[i].name[:-1]))
                del fleet.ships[i]
                return 1
        return 0

    def printstats(self):
        listy = []
        import Shipfolder
        s: Shipfolder.ship_f.Ship
        for s in self.ships:
            s.hp = [s.ship_shield.hp, s.ship_armor.hp, s.ship_hull.hp]
            if s.current_target == None:
                print("%-20s %-20s %-20s %-5d %-5d %-5d %-10s %-25s %-20s %-15s %-25s" %
                      (s.name[:-1], self.name, str(s.hp), s.loc.x, s.loc.y, s.loc.z, s.is_anchor, "None", s.distance_from_target, s.damage_dealt_this_tick, s.angular_velocity))
                listy.append(("%-20s %-20s %-20s %-5d %-5d %-5d %-10s %-25s %-20s %-15s %-25s" %
                              (s.name, self.name[:-1], str(s.hp), s.loc.x, s.loc.y, s.loc.z, s.is_anchor, "None", s.distance_from_target, s.damage_dealt_this_tick, s.angular_velocity)))
            else:
                print("%-20s %-20s %-20s %-5d %-5d %-5d %-10s %-25s %-20s %-15s %-25s" % (s.name[:-1], self.name, str(s.hp), s.loc.x, s.loc.y, s.loc.z, s.is_anchor, s.current_target.name[:-1],s.distance_from_target, s.damage_dealt_this_tick,s.angular_velocity))  # [:-1] is for the names.... why do these have /n's? why why why
                listy.append(("%-30s %-20s %-20s %-5d %-5d %-5d %-10s %-25s %-20s %-15s %-25s" % (
                s.name[:-1], self.name, str(s.hp), s.loc.x, s.loc.y, s.loc.z, s.is_anchor, s.current_target.name,
                s.distance_from_target, s.damage_dealt_this_tick, s.angular_velocity)))
        return listy
