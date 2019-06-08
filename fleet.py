import weakref
from ship import *
class fleet():
    fleets = []

    def __init__(self,name):
        self.__class__.fleets.append(weakref.proxy(self)) #all fleets are tracked because why not
        self.name = name
        self.ships = []
        self.is_anchor = False
        self.currentanchor = None
        self.currenttargetstatus = -1  #-1 Not set, 0 is dead, 1 is alive
        self.currentprimary = None
        z = 0
        y = 0
        z = 0
        self.anchor_goto_loc = location(0,0,0)
        self.engagementrange = None
        self.anchordistance = 2000
        self.fleet_capitulation_status = 0
        self.engagementrange = 1500 #place holder value todo: fix this please

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

    def add_ship_to_fleet(self,ship):
        self.ships.append(ship)

    def remove_ship(self,ship,reason):
        for i in self.ships:
            if i.name == ship.name:
                del i


    def listallfleetmembers(self):
        fleetmembers = ""
        count = 0
        for i in self.ships:
            fleetmembers += "%s %s %s %s %s %s\n"(str(count),str(i.name),str(i.hp),str(i.loc.x),str(i.loc.y),str(i.loc.z))
        return fleetmembers

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
    def anchor_move_to_target(self,target):
        pass

    def anchorup(self):
        not_everyone_anchored = False
        for i in range(0, len(self.ships)):
            if self.ships[i].is_anchor == True:
                if self.currentprimary == None:
                    print("No Primary selected!")
                elif self.currentanchor.check_range(self.currentprimary) > self.engagementrange:
                    self.currentanchor.move_ship_to(self.currentprimary)
                continue
            if self.ships[i].calc_distance(self.currentanchor) > self.anchordistance: #distance should be 5000
                self.ships[i].move_ship_to(self.currentanchor)
                not_everyone_anchored = True
        if not_everyone_anchored == True:
            return 0  #GODDAMN TRYRM GUYS
        else:
            return 1  #If everyone is anchored and in range - we get a return 1 and PGL is happy


    def chooseprimary(self,fleet,method):
        distances = []
        for ship in range(0,len(fleet.ships)):
            distances.append(self.currentanchor.calc_distance(fleet.ships[ship]))
        return fleet.ships[np.argmin(distances)]

    def fleet_choose_primary_now(self,fleet,method):
        distances = []
        for ship in range(0, len(fleet.ships)):
            distances.append(self.currentanchor.calc_distance(fleet.ships[ship]))
        self.currentprimary = fleet.ships[np.argmin(distances)]

    def fleet_attack_procedure(self,target): #based off the ship class
        if debug == 1:
            print("Debug - main_attack_procedure\nRange of " + self.name + " to " + target.name + " :" + str(self.check_range(target)))
        if self.check_range(target) > self.range:
            self.currentanchor.move_ship_to(target)
        else:
            self.attack(target)

    def attack_primary(self):
        for ships in self.ships:
            ships.current_target = self.currentprimary
            ships.main_attack_procedure(self.currentprimary)

    def attack_other_fleet(self,fleet,method):
        if method == "Basic Anchor and attack":

            if(self.currenttargetstatus != 1): #If our ship is not alive
                self.currentprimary = self.chooseprimary(fleet,"closest")




            if self.currentprimary.hp >0:
                self.currenttargetstatus = 1
                #attack if in range
                for i in range(0,len(self.ships)):
                    self.ships[i].current_target = self.currentprimary
                    self.ships[i].main_attack_procedure(self.currentprimary,self)

            elif self.currentprimary.hp <= 0:
                self.currenttargetstatus = 0


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
    def choosenewanchor(self):
        hp = []
        for i in range(0,len(self.ships)):
            hp.append(self.ships[i].hp)
        self.set_anchor(self.ships[np.argmax(hp)])
        #return fleet.ships[np.argmin(distances)]


    def checkenemyfleetdead(self,fleet):
        for i in range(0, len(fleet.ships)):
            if fleet.ships[i].hp <= 0:
                if fleet.currentanchor == fleet.ships[i]:
                    fleet.choosenewanchor()
                del fleet.ships[i]
                return 1
        return 0


    def printstats(self):
        listy = []

        for s in self.ships:
            if s.current_target == None:
                print("%-20s %-10s %-10d %-5d %-5d %-5d %-10s %-25s %-20s %-15s %-25s" % (
                s.name[:-1], self.name, s.hp, s.loc.x, s.loc.y, s.loc.z, s.is_anchor, "None",
                s.distance_from_target, s.damagedealt_this_tick, s.angular_velocity))
                listy.append(("%-20s %-10s %-10d %-5d %-5d %-5d %-10s %-25s %-20s %-15s %-25s" % (
                s.name, self.name[:-1], s.hp, s.loc.x, s.loc.y, s.loc.z, s.is_anchor, "None",
                s.distance_from_target, s.damagedealt_this_tick, s.angular_velocity)))
            else:
                print("%-20s %-10s %-10d %-5d %-5d %-5d %-10s %-25s %-20s %-15s %-25s" % (s.name[:-1], self.name, s.hp, s.loc.x, s.loc.y, s.loc.z, s.is_anchor,s.current_target.name,s.distance_from_target,s.damagedealt_this_tick,s.angular_velocity))
                listy.append(("%-30s %-10s %-10d %-5d %-5d %-5d %-10s %-25s %-20s %-15s %-25s" % (s.name, self.name, s.hp, s.loc.x, s.loc.y, s.loc.z, s.is_anchor,s.current_target.name,s.distance_from_target,s.damagedealt_this_tick,s.angular_velocity)))
        return listy