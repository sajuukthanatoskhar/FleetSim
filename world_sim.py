import collections
import math
from typing import List

import fleet
from fleet import *
import socket
from players import *
from UDP_Server_Client.Server_Client import *
import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D
import Pyro4
import threading
import os
import Shipfolder.ship_f
import json
from world_config import WorldStates, FleetStates, WorldConfig, MenuMessages

DEBUG = False


# class World_Timer:
#

class World:
    """
    Defines the players, the ports, server
    """

    def __init__(self, numplayers):
        """
        Initialises the world, number of players, ports and server particulars
        :param numplayers: Number of players who are playing
        :param time_dilation: Delay between next eve sim second, 1.0 is one real time second per eve tick, 0.1 is 10 eve seconds for one real time second
        """
        self.capitulationstatus = 0
        self.sim_timer = 0  # simulation ticker, it represents the global time scale
        self.UDP_port_no = 6789
        self.Sender_Port_No = 6790
        self.UDP_IP_Address = "127.0.0.1"
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversock.bind(("", self.UDP_port_no))  # We are listening on 6789
        self.remoteip = "192.168.178.22"
        self.listenersock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Howmanyplayers = numplayers

        self.fleets = []
        self.ships = []
        self.playersplaying: List[Players_c] = []
        self.fleet_capitulation_status = FleetStates.fleet_combat_effective  # Look to Fleetstates
        self.time_dilation = WorldConfig.time_dilation_factor

    def check_fleet_status(self) -> None:
        """
        Checks if the fleet is still active or not
        :return: None
        """
        for players in self.playersplaying:
            for singleplayerfleets in players.owned_fleets:
                if singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_combat_effective:
                    processing_dead = 1
                    while processing_dead:
                        processing_dead = singleplayerfleets.checkenemyfleetdead(singleplayerfleets)
                        if not singleplayerfleets.ships:
                            singleplayerfleets.fleet_capitulation_status = FleetStates.fleet_capitulated
                            print(
                                f"Status Update: Player {players.name}: Fleet {singleplayerfleets.name} -- Fleet capitulated")

                elif singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_capitulated:
                    print(f"Status Update: Player {players.name}: Fleet {singleplayerfleets.name} -- Fleet capitulated")

            playerfleet: fleet.Fleet
            # everything must be dead from that players fleet or capitulated
            if not any([playerfleet.fleet_capitulation_status for playerfleet in players.owned_fleets]):
                players.player_state = PlayerState.AllFleetCapitulated
                self.message_to_all_players(f"{players} has no more fleets!")

    def anchor_movephase(self) -> None:
        """
        All fleets will move/anchor
        :return: None
        """
        i: Fleet
        for i in range(0, len(self.fleets)):
            i.anchorup()

    def attack_phase(self):
        """
        Process all fleets attacking
        :return: None
        """
        pass

    def destroyed_ships_processing(self):
        """
        Process all ships below <0 hull/hp
        :return:
        """
        pass

    def present_fleetchoices(self):
        """

        :return:
        """
        pass

    def load_fleets(self):
        """
        Loads the fleet up for each players
        :return:
        """
        for player in self.playersplaying:
            print("%s having fleets loaded...\n" % player.name)
            self.loadplayerfleets(player)
        print("Loading Players 100 km from each other")

        for count, players in enumerate(self.playersplaying):
            for singleplayerfleets in players.owned_fleets:
                self.spawn_player_ship(count, singleplayerfleets)
                singleplayerfleets.fleet_capitulation_status = FleetStates.fleet_combat_effective
                self.setanchorforplayer_fleet(players, singleplayerfleets)
                # singleplayerfleets.printstats()
            print(count)
        print("loaded players")

    def spawn_player_ship(self, count: int, singleplayerfleets: Fleet):
        """
        Spawns the player's fleet and places them in position
        :param count:
        :param singleplayerfleets:
        :return:
        """
        for spawning_ship in singleplayerfleets.ships:  # spawning ship is the ship being spawned in
            spawning_ship.loc.x = 100000 * math.cos(3.14 * count / len(self.playersplaying)) + random.randint(
                -3, 3)
            spawning_ship.loc.y = 0 + 2500 * random.randint(-6, 6)
            spawning_ship.loc.z = 0 + 2500 * random.randint(-6, 6)

    def ship_allocation(self) -> None:
        """
        Allocates ships to a fleet
        :return:
        """
        for i in self.playersplaying:
            choice = -1
            while (choice != -2):
                fleetchoices = self.view("fleet")
                Fleetstring = ""
                for j in range(0, len(fleetchoices)):
                    Fleetstring = str(j) + ". " + fleetchoices[j] + "\n"
                message = "\nPlayer, which fleet do you want?  If you don't want to add a fleet, do -2"
                message = Fleetstring + message
                self.listenersock.sendto(message.encode("utf-8"), (i.address, int(i.port)))
                data, address = self.serversock.recvfrom(1024)
                # if choice.isdigit() & int(choice) > -1 & int(choice) < len(fleetchoices):
                choice = int(data)
                print(data)
                if int(choice) > -1 and int(choice) < len(fleetchoices):
                    i.add_fleet(fleetchoices[choice])
                elif int(choice) == -2:
                    choice = -2

    def worldstate(self, world_state_val: int) -> int:
        """

        :param world_state_val:
        :return:
        """
        if world_state_val == WorldStates.preload_ips_players:
            while world_state_val == WorldStates.preload_ips_players:
                print("**** Collecting players and IPs ****")
                self.collect_ip_players()
                if len(self.playersplaying) == self.Howmanyplayers:
                    world_state_val = WorldStates.player_allocation
        if world_state_val == WorldStates.player_allocation:
            count = 0
            print("**** Allocating Fleets to players, please wait ****")
            for player in self.playersplaying:
                playerreceived = player.name
                print(player.name + " " + player.address + " " + player.port)
                self.listenersock.sendto(playerreceived.encode("utf-8"), (player.address, int(player.port)))
                data, addr = self.serversock.recvfrom(1024)
                data = data.decode('utf-8')
                if data == "ok":
                    count = 1 + count
            print(f"Player Count = {count}")
            world_state_val = WorldStates.initialise_fleets

        if world_state_val == WorldStates.initialise_fleets:
            statechoice = -1
            while statechoice == -1:  # Printing out each player, IP and fleets
                print("%-30s %-20s %-50s" % ("Player Name", "Address", "Owned Fleets\n"))
                for i in range(0, len(self.playersplaying)):
                    ownedshipslist = ""
                    for j in range(0, len(self.playersplaying[i].owned_fleets)):
                        ownedshipslist = ownedshipslist + "," + self.playersplaying[i].owned_fleets[j]
                    print("%-30s %-20s %-50s" % (
                        self.playersplaying[i].name, self.playersplaying[i].address, str(ownedshipslist)))

                self.ship_allocation()
                statechoice = 0
                world_state_val = WorldStates.Fleet_Combat_State
        if world_state_val == WorldStates.Fleet_Combat_State:
            self.load_fleets()
            plt.ion()
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')

            self.sim_timer = 0

            while self.IsActivePlayers():
                """
                Check if there are active players still"""
                self.fleet_combat_check_all_players_fleets()

                self.move_ships_in_world()
                self.all_fleets_in_world_attack()
                self.printing_fleet_ships()
                self.check_fleet_status()
                self.Update_GUI_Interface_And_Ship_Positions(ax)

                # if len([player.player_state for player in self.playersplaying if
                #         player.player_state == PlayerState.FleetsActive]) <= 1:

                world_state_val = self.IsActivePlayers()

                if DEBUG:
                    for players in self.playersplaying:
                        self.listenersock.sendto("End:Send p to continue".encode('UTF-8'),
                                                 (players.address, int(players.port)))
                        data, addr = self.serversock.recvfrom(1024)

                if world_state_val == WorldStates.end_of_fight:
                    break

        return world_state_val

    def fleet_combat_check_all_players_fleets(self):
        for players in self.playersplaying:
            self.fleet_combat_check_player_fleet(players)

    def fleet_combat_check_player_fleet(self, players) -> None:
        """
        Checks that the status of all fleets of a player are checked
        :return None:
        """
        for singleplayerfleets in players.owned_fleets:
            if singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_combat_effective:
                if singleplayerfleets.currentprimary is None or singleplayerfleets.currentanchor == None:
                    if singleplayerfleets.currentanchor is None:
                        message = f"NoAnchor:{singleplayerfleets.name} Anchor - None\n{singleplayerfleets.listallfleetmembers()}"
                        self.listenersock.sendto(message.encode("utf-8"),
                                                 (players.address, int(players.port)))
                        self.message_to_all_players("Pausing Game for Anchor Change")
                        data, addr = self.serversock.recvfrom(1024)
                    if singleplayerfleets.currentprimary is None:
                        message = f"NoPrimary:{singleplayerfleets.name} Primary - None\n" \
                                  f"{self.listofvalidprimaries(singleplayerfleets)}"
                        self.listenersock.sendto(message.encode("utf-8"),
                                                 (players.address, int(players.port)))
                        self.message_to_all_players("Pausing Game for Primary Change for %s" % players)
                        data, addr = self.serversock.recvfrom(1024)
                        while data.decode() == 'p':  # todo: check for hex address
                            data, addr = self.serversock.recvfrom(1024)
                        print("%s" % data)
                        singleplayerfleets.currentprimary = findshipbymemaddress(singleplayerfleets,
                                                                                 data.decode())
                        singleplayerfleets.currentanchor.current_target = singleplayerfleets.currentprimary



            elif singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_capitulated:
                print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                    players.name, singleplayerfleets.name))

    def Update_GUI_Interface_And_Ship_Positions(self, ax):
        """
        Updates positions on 3D Interface
        :param ax:
        :return None:
        """
        for players in self.playersplaying:
            for singleplayerfleets in players.owned_fleets:
                for shipd in singleplayerfleets.ships:
                    ax.scatter(shipd.loc.x, shipd.loc.y, shipd.loc.z, c=singleplayerfleets.color, marker=shipd.marker)
        self.sim_timer += 1
        plt.pause(self.time_dilation)
        plt.cla()
        plt.xlim([-100000.0, 100000.0])
        plt.ylim([-100000.0, 100000.0])
        plt.draw()


    def printing_fleet_ships(self) -> None:
        for players in self.playersplaying:
            print("Sim Timer --> {}".format(self.sim_timer))
            line = Shipfolder.ship_f.printstatsheader()
            for singleplayerfleets in players.owned_fleets:
                if singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_combat_effective:
                    i: Shipfolder.ship_f.Shipfolder
                    for i in singleplayerfleets.ships:
                        if i.damage_dealt_this_tick > 0:
                            pass
                            # print("Damage: %d for %s"%(int(i.damagedealt_this_tick),str(i.name)))

                    self.listenersock.sendto(line.encode('UTF-8'), (players.address, int(players.port)))
                    listy = singleplayerfleets.printstats()
                    for i in range(0, len(listy)):
                        self.listenersock.sendto(listy[i].encode('UTF-8'), (players.address, int(players.port)))
                elif singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_capitulated:
                    print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                        players.name, singleplayerfleets.name))

    def all_fleets_in_world_attack(self) -> None:
        for players in self.playersplaying:
            for singleplayerfleets in players.owned_fleets:
                if singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_combat_effective:
                    singleplayerfleets.attack_primary()
                elif singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_capitulated:
                    print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                        players.name, singleplayerfleets.name))

    def move_ships_in_world(self) -> None:
        """
        Moves all the ships in the world to where they want to be
        :return:
        """
        for players in self.playersplaying:
            for singleplayerfleets in players.owned_fleets:
                if singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_combat_effective:
                    if (len(singleplayerfleets.ships)) > 0:
                        singleplayerfleets.anchorup()
                elif singleplayerfleets.fleet_capitulation_status == FleetStates.fleet_capitulated:
                    print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                        players.name, singleplayerfleets.name))

    def collect_ip_players(self) -> None:
        """
        Collects all players and their ip's
        :return:
        """
        data, addr = self.serversock.recvfrom(1024)
        data = data.decode("utf-8")
        if "fleetplayer" in data:
            # format will be 'fleetplayer,name'
            massdata = data.split(',')
            self.playersplaying.append(Players_c(str(massdata[1]), str(addr), str(massdata[2])))
            for i in massdata:
                print("{}".format(i))

    @staticmethod
    def make_new_ship_spec() -> dict:
        import ast
        ship_dict = {}
        try:
            ship_dict = ast.literal_eval(
                input("\nCopy and Paste the pyfa EFS (Fit -> Copy To -> Select a Format (EFS) -> Ok)"))
        except Exception as e:
            print("Exception occurred : {}".format(e))
            ship_dict = {"Error": e}
        finally:
            return ship_dict

    def buildfleet(self):
        """
        Builds more than just fleets
        :return:
        """
        state = -1
        while (True):
            state = input("1. Design Fleet\n2. Design Ships\n3. Design Weapon\n4. Verify Pyfa EFS import"
                          "\n5. View Fleets made\n6. View Ships made\n7. Go back")
            if state == '1':
                fleetname = input("Name of Fleet? $ ")
                shipsinfleet = []
                numshipsinfleet = []
                shiplist = self.view("ship")
                choice = -1
                while choice == -1:
                    choice = -1

                    while (int(choice) <= -1 or int(choice) >= len(shiplist) - 1):
                        print("%15s\t%10s\t%10s\t%10s\t%10s\t%10s" % (
                            "Ship Name", "HP", "Target Range", "Max Speed", "Signature", "Turret"))
                        for i in shiplist:
                            filet = open(i, 'r')
                            content = filet.readlines()
                            # todo print out optimal falloff and dps
                            print("%15s\t%10s\t%10s\t%10s\t%10s\t%10s" % (
                                content[0][:-1], content[1][:-1], content[2][:-1], content[3][:-1], content[4][:-1],
                                content[5][:-1]))

                        choice = int(input("Choose a ship type for the fleet"))

                        if (choice <= -1 or choice >= len(shiplist)):
                            print("\nError:Choose a valid number!\n")
                            choice = -1
                            continue
                        else:
                            number = input('How many ships in fleet? $ ')
                            shipsinfleet.append(shiplist[choice])
                            numshipsinfleet.append(number)
                            while (True):
                                wantmorequery = input("Need more ships for fleet?  ")
                                if wantmorequery == 'y' or wantmorequery == 'n':
                                    if wantmorequery == 'y':
                                        choice = -1
                                        continue
                                    if wantmorequery == 'n':
                                        choice = 0
                                        break
                                else:
                                    print("Error")

                with open(fleetname + ".fleet", "w+") as f:
                    f.write(str(fleetname))

                    if len(shipsinfleet) == len(numshipsinfleet):
                        f.write("\n" + str(len(shipsinfleet)))
                        for i in range(0, len(shipsinfleet)):
                            f.write("\n" + str(shipsinfleet[i]) + " " + str(numshipsinfleet[i]))
            if state == '2':  # todo: redo ship stuff here
                # todo: Add in confirmation before write
                shipspecs_dict = self.make_new_ship_spec()
                filename = "".join(filter(str.isalnum, shipspecs_dict['name']))
                with open("{}.ship".format(filename), "w+") as f:
                    f.write(json.dumps(shipspecs_dict))
                    f.close()

            if state == '3':
                # Deprecated: No more weapon generation, I hated this with a passion.  - STK
                print("Deprecated")
            if state == '4':
                print("This is to test the import of the EFS of a file")
                self.validate_pyfa_EFS()
            if state == '5':
                self.view('fleet')
            if state == '6':
                self.view('ship')
            if state == '7':
                print("Deprecated")  # Deprecated: No more weapon generation, I hated this with a passion.  - STK
                return -1

    def view(self, param: str) -> list:
        """
        Presents a list of files based on what param is

        :param param: can be 'ship' or 'fleet' or 'weapon'
        :return: a list of param.file filenames to refer to that were saved
        """
        availabilitylist = []  # for shipcreation
        count = 0
        print('\n***********************************************************\n\nSaved %ss\n-----------' % param)
        for i in os.listdir():
            if '.' + param in i:
                availabilitylist.append(i)
                print(str(count) + ". " + i)
                count = count + 1
        print('******************************************************************')
        return availabilitylist

    # def give_fleets(self):
    #     #todo players will receive a signal signalling what fleets there are, there should be a summary of things maybe
    #     pass

    def loadplayerfleets(self, player):
        count = 0
        for fleet in player.owned_fleets:
            player.owned_fleets[count] = player.populatefleet(fleet)
            count += 1

    def setanchorforplayer_fleet(self, players, singleplayerfleets):
        setanchormsg = f"{players.name} is being requested to select an anchor..."
        self.message_to_all_players(setanchormsg)
        singleplayerfleets.choosenewanchor()

    def message_to_all_players(self, setanchormsg: str):
        """
        Messages all players
        :param setanchormsg:
        :return:
        """
        for playerstobemessage in self.playersplaying:
            self.listenersock.sendto(setanchormsg.encode("utf-8"),
                                     (playerstobemessage.address, int(playerstobemessage.port)))

    def listofvalidprimaries(self, player=None):
        """
        The ships, their addresses are located printed via here.  This currently is bugged
        Bare in mind, that there is a list of all ships in the world.  This list is not updated ever.
        :param: This is the player that hasn't got a primary for their fleet
        :return: a list of ships todo: like wtf is this - could just put this in a list of list
        """
        # we want player,distance,shiptype
        count = 0
        listofships = ""

        for players in self.playersplaying:
            if players == player:
                continue
            for singleplayerfleets in players.owned_fleets:
                for individualships in singleplayerfleets.ships:
                    # print("%s %s %s %s %s" %(str(count), individualships.name,str(individualships.loc.x),str(individualships.loc.y),str(individualships.loc.z)))
                    listofships += "%s %s %s %s %s %s %s\n" % (
                        str(count), individualships.name[:-1], players.name, str(individualships.loc.x),
                        str(individualships.loc.y), str(individualships.loc.z), str(hex(id(individualships))))
        return listofships

    def validate_pyfa_EFS(self):
        """
        Validates PYFA EFS
        :return:
        """
        pass

    def IsActivePlayers(self):
        """Gets all active fleets for each player, maybe move to player class"""
        player : Players_c
        player_fleet : Fleet
        for player in self.playersplaying:
            fleetstatuses = [player_fleet.fleet_capitulation_status for player_fleet in player.owned_fleets]
            if FleetStates.fleet_combat_effective in fleetstatuses:
                player.player_state = PlayerState.FleetsActive
            else:
                player.player_state = PlayerState.AllFleetCapitulated

        players_states = collections.Counter([activeplayers.player_state for activeplayers in self.playersplaying])

        if players_states[PlayerState.FleetsActive] < 2:
                return False
        else:
            return True

def printMMD():
    print("                                                          .-:-°\n\
                                                        °omysyhy/°°°°   °-/o:°\n\
                                                       :dNhsoo+/sddhhhhhdhh/hy°\n\
                                                     -ymdyyhhmmh+/yyyyyssyy-.M-\n\
                                                  °-smdyyyhhhNMNmyossssso:-°.M°\n\
                               °.-/++oooo++++++/:ohdhyyyhhhhhdNNNdyyssssss+.-M/\n\
                              -hhsoo+ooosssoooosyhmmdhhhhhhhhhhhhhhhyyssssss:sN/\n\
                              +Mdossyhhhhhhhyssooosydddhhyyyyyyyyhhhhhyssssss:sN/\n\
                              .NMdhdmmmNhhhdMmssssyyyhhhhhhhyyysssyhhhhyssssss.yN/\n\
                               dMmysyyhm.°.oMmssyyhhhhhhhhhhhhhhyyyyhhhhyssssso.hN-\n\
                             °.oMmyssshNdhdmMNyyhhhhhhhhhhhhhhhhhhhyhhhhhysssss+-Nh\n\
                           -shhNNdhyyhhhdddNMmhhhhhhhhhhhhhhhhhddhhhhhhhhhyyyyss:sN.\n\
                          oNdsoNdhhhhhhdmNNNmhhhhhhhdhhhhddhhhhNyddddddddhhhhhyysoM-\n\
                         .NdsyddhhhhhhdddddhhhhhhhhdmmmdmhhmNNNNdsdm/-dNNmmmdhmdymd.\n\
                         +Mhyhhhhhhhhhhhhhhhhhhhhhhdh/hN/ °hddhhddmm/sdyyhdN+°hNhoosn\n\
                         sMhhhyyssyyyhhhhhhhhhhhhhyhNdmm/ hdhhhhhhhdmmyysyhNsyMy-oo°\n\
                         +MdhhsssssssyyhhhhhhhhyyydMNNmNy+mhhhhhhhhhhhhhssshhyNms-\n\
                         :MmhysssyyysssyyyyyyssyyNMNdhhdNNhhhhhhhhhhhhhhyssssyN+\n\
                         .MmhssyyhhhyyhhhhyyyhdmNNmhhysshNhhhhhhhhhhhhhyssyyhNd°\n\
                          NNysyhhhhyhNmmmmNNNNNmdhhhysssyyyyyyhhhhhhhyyyyhdNmo°\n\
                          dNysyhhdmhmhhhhhhhhhhhhhysssssyyhhhhhhhhyyyhmdyo/.\n\
                          sMyyyhhdNmhhhyyyyyyyyyyssssyyhhhhhhhhhyydmdoNo\n\
                          /MhymyhdNdhyysssssssssssyyhhyyhhhhhhhyddhss-N:\n\
                          -Mdymdyhmmhhhyssssssyyhhhhyyyhhhhhhhyhhhys-om°\n\
                          °NmydNyhhmdhhysssyyhhhhyyhhdhhhhhhhhhhyss:-N-\n\
                           mNyhdNyyhhhyyssyhhhhhdddhhhhhhhhhhhysss::m/\n\
                          -mNyhhmmyyyssssyhddmNNdhhyyyhhhhhhyyss+.om/\n\
                       -ohmdMyyhhmNdhyhhdmNmdhyyyysyhddmmmmdhho/+dy-\n\
                      :NMN/+MysyhhhmNmmddhyyysssyyhhhhhhhyyhydNhs-°\n\
                      .NMm.°NmysyhhyNdhysssssyyhhhhhhhhhhyso.hhms-\n\
                       mMMs°-hmyyyhhhNdhyyyyhhhhhhhhhhhhyso-yhyN/h-\n\
                      °NMMNo°°-shhhhhhmdhhhhhhhhhhhhhhhyyyhddho. s/\n\
                      sMMMMNy-° °./shhdNmmmmmmddddhhhddhys+:.°   dh°\n\
                     :NMMMMMNmy/.   °°....-....-yymdmNdds.      +hmh°\n\
                     /mmNMMMMMNNho-°          °yNdmmmmmmNy°    :Nyoyh°\n\
                      sdhmNMMMMMMNmh+.°       oNhhhhhhhooN+   :hmm-m+y\n\
                      :NmhhmNMMMMMMMNds/-.°   mNmhyhmmmhsNd°.oNd+yyMsy+\n\
                      oMMNmhdmNMMMMMMMNmdhs+:-mdhddNdddsmdmo/.mMNdsod-m.\n\
                     .NMMMMMNdhmMMMMMMMMMNddmdmy:.:Nhhhy/d:° °NMMMMyhsoh°\n\
                    °yNNMMMMMMNMMMMMMMMMMNNhy:.°  smhhhhoo+  -MMMMMmNN-m+\n\
                    omyNMMMMMmhmMMMMMMMMMNdhh.   :dhhhhhh+y/ +MMMMMMMMy:N.\n\
                   .hooyddddddyoydddddddddds+/  .yyyyyyyys:h/hddddddddd-ss\n\
                    °   °°°°°°°  °°°°°°°°°°° °              °°°°°°°°°°°  °                          ")


def findshipbymemaddress(singleplayerfleets, data):
    for fleets in singleplayerfleets.fleets:
        for ships in fleets.ships:
            if data == hex(id(ships)):
                return ships


def start_nameserver(mainworldobject):
    Pyro4.Daemon.serveSimple({mainworldobject: "mainserver"}, ns=True, )


if __name__ == "__main__":
    main_world = World(2)
    state = 0
    printMMD()
    while (True):
        menu_state = input("\n\nTEST Alliance Fleet Simulator\n"
                           "1.\tMake fleet?\n"
                           "2.\tBattlefleets?\n"
                           "3.\tQuit\n"
                           "Make your choice, Fleet Commander of Test... \n $ ")
        if menu_state == '1':
            main_world.buildfleet()

        if menu_state == '2':
            state = main_world.worldstate(state)
            print(MenuMessages.menu_fleetcombat[f'{state}'])
            state = 0

        if menu_state == '3':
            break
