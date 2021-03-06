import math

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




class World:
    def __init__(self, numplayers):
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
        self.playersplaying = []
        self.fleet_capitulation_status = 0  # 0 is still active fleet, 1 is dead fleet

    ''''''

    def anchor_movephase(self) -> None:
        """
        All fleets will move/anchor
        :return: None
        """
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

    def ship_allocation(self):
        """
        Allocates ships
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

    def worldstate(self, world_state_val):
        if world_state_val == 0:
            while world_state_val == 0:
                print("collecting players and IPs")
                self.collect_ip_players()
                if len(self.playersplaying) == self.Howmanyplayers:
                    world_state_val = 1
        if world_state_val == 1:
            count = 0
            print("\nAllocating Fleets to players, please wait")
            for player in self.playersplaying:
                print(player.name)
                playerreceived = player.name
                print(player.name + " " + player.address + " " + player.port)
                self.listenersock.sendto(playerreceived.encode("utf-8"), (player.address, int(player.port)))
                data, addr = self.serversock.recvfrom(1024)
                data = data.decode('utf-8')
                if data == "ok":
                    count = 1 + count
            print("count = %s" % str(count))
            world_state_val = 2

        if world_state_val == 2:
            statechoice = -1
            while (statechoice == -1):  # Printing out each player, IP and fleets
                print("%-30s %-20s %-50s" % ("Player Name", "Address", "Owned Fleets\n"))
                for i in range(0, len(self.playersplaying)):
                    ownedshipslist = ""
                    for j in range(0, len(self.playersplaying[i].owned_fleets)):
                        ownedshipslist = ownedshipslist + "," + self.playersplaying[i].owned_fleets[j]
                    print("%-30s %-20s %-50s" % (
                    self.playersplaying[i].name, self.playersplaying[i].address, str(ownedshipslist)))

                self.ship_allocation()  # todo players need to get fleets.
                statechoice = 0
                world_state_val = 3
        if world_state_val == 3:

            for player in self.playersplaying:
                print("%s having fleets loaded...\n" % player.name)
                self.loadplayerfleets(player)
            print("Loading Players 100 km from each other")

            capitulationstatus = 0
            count = 0
            for players in self.playersplaying:  # todo: put in function
                for singleplayerfleets in players.owned_fleets:
                    for shippyships in singleplayerfleets.ships:  # I can't remember if there is a naming conflict for any of these
                        shippyships.loc.x = 100000 * math.cos(3.14 * count / len(self.playersplaying)) + random.randint(
                            -3, 3)
                        shippyships.loc.y = 0 + 2500 * random.randint(-6, 6)
                        shippyships.loc.z = 0 + 2500 * random.randint(-6, 6)
                    self.setanchorforplayer_fleet(players, singleplayerfleets)
                    # singleplayerfleets.printstats()
                count += 1
                print(count)

            # todo: then after the loading, they need to be placed on the field, given an anchor

            # todo: we do battle ehre, all players should have their fleets at this point.   The word needs to set up a battle arena .
            # todo: need anchor for
            print("loaded players")
            plt.ion()
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            self.sim_timer = 0
            while (True):
                for players in self.playersplaying:
                    for singleplayerfleets in players.owned_fleets:
                        if singleplayerfleets.fleet_capitulation_status == 0:
                            if singleplayerfleets.currentprimary == None or singleplayerfleets.currentanchor == None:
                                if singleplayerfleets.currentanchor == None:
                                    message = "NoAnchor:%s Anchor - None\n%s" % (
                                    singleplayerfleets.name, singleplayerfleets.listallfleetmembers())
                                    self.listenersock.sendto(message.encode("utf-8"),
                                                             (players.address, int(players.port)))

                                    self.message_to_all_players("Pausing Game for Anchor Change")
                                    data, addr = self.serversock.recvfrom(1024)
                                if singleplayerfleets.currentprimary == None:
                                    message = "NoPrimary:%s Primary - None\n%s" % (
                                    singleplayerfleets.name, self.listofvalidprimaries())
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
                                    # singleplayerfleets.currentprimary =
                                    # data, address = self.serversock.recvfrom(1024)


                        elif singleplayerfleets.fleet_capitulation_status == 1:
                            print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                            players.name, singleplayerfleets.name))

                # For loop for moving ships and anchors#todo: check code
                self.move_ships_in_world()
                # For loop for attacking ships #todo: check code
                self.all_fleets_in_world_attack()

                # For loop for printing fleet ships #todo: check code
                self.printing_fleet_ships()

                # if ships from a fleet are dead - set capitulation status
                for players in self.playersplaying:
                    for singleplayerfleets in players.owned_fleets:
                        if singleplayerfleets.fleet_capitulation_status == 0:
                            processing_dead = 1
                            while (processing_dead):
                                processing_dead = singleplayerfleets.checkenemyfleetdead(singleplayerfleets)
                                if not singleplayerfleets.ships:
                                    singleplayerfleets.fleet_capitulation_status = 1
                                    print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                                        players.name, singleplayerfleets.name))
                                    return 2
                        elif singleplayerfleets.fleet_capitulation_status == 1:
                            print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                            players.name, singleplayerfleets.name))
                            # todo: remove fleet
                            return 2

                for players in self.playersplaying:
                    for singleplayerfleets in players.owned_fleets:
                        for shipd in singleplayerfleets.ships:
                            ax.scatter(shipd.loc.x, shipd.loc.y, shipd.loc.z, c=singleplayerfleets.color, marker=shipd.marker)
                self.sim_timer += 1
                plt.pause(0.1)
                plt.cla()
                plt.draw()


                # for players in self.playersplaying:
                #     self.listenersock.sendto("End:Send p to continue".encode('UTF-8'), (players.address, int(players.port)))
                #     data, addr = self.serversock.recvfrom(1024)

                # todo: do things
                # print("loaded Fleets, awaiting battle")
        '''
        #todo:eed to fill in the following
        allow players to set anchors
        allow players to move fleets
        allow players to toggle attacking
        allow players to set primary
        '''

        return world_state_val

    def printing_fleet_ships(self):
        for players in self.playersplaying:
            print("Sim Timer --> {}".format(self.sim_timer))
            line = Shipfolder.ship_f.printstatsheader()
            for singleplayerfleets in players.owned_fleets:
                if singleplayerfleets.fleet_capitulation_status == 0:
                    i: Shipfolder.ship_f.Shipfolder
                    for i in singleplayerfleets.ships:
                        if i.damage_dealt_this_tick > 0:
                            pass
                            # print("Damage: %d for %s"%(int(i.damagedealt_this_tick),str(i.name)))

                    self.listenersock.sendto(line.encode('UTF-8'), (players.address, int(players.port)))
                    listy = singleplayerfleets.printstats()
                    for i in range(0, len(listy)):
                        self.listenersock.sendto(listy[i].encode('UTF-8'), (players.address, int(players.port)))
                elif singleplayerfleets.fleet_capitulation_status == 1:
                    print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                        players.name, singleplayerfleets.name))

    def all_fleets_in_world_attack(self):
        for players in self.playersplaying:
            for singleplayerfleets in players.owned_fleets:
                if singleplayerfleets.fleet_capitulation_status == 0:
                    singleplayerfleets.attack_primary()
                elif singleplayerfleets.fleet_capitulation_status == 1:
                    print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                        players.name, singleplayerfleets.name))

    def move_ships_in_world(self):
        """
        Moves all the ships in the world to where they want to be
        :return:
        """
        for players in self.playersplaying:
            for singleplayerfleets in players.owned_fleets:
                if singleplayerfleets.fleet_capitulation_status == 0:
                    if (len(singleplayerfleets.ships)) > 0:
                        singleplayerfleets.anchorup()
                elif singleplayerfleets.fleet_capitulation_status == 1:
                    print("Status Update: Player %s: Fleet %s -- Fleet capitulated" % (
                        players.name, singleplayerfleets.name))

    def sendfleetdata(self, type, player):
        if type == "Anchor select":
            pass
        if type == "big list":
            pass

    def collect_ip_players(self):
        data, addr = self.serversock.recvfrom(1024)
        data = data.decode("utf-8")
        if "fleetplayer" in data:
            # format will be 'fleetplayer,name'
            massdata = data.split(',')
            self.playersplaying.append(Players_c(str(massdata[1]), str(addr), str(massdata[2])))
            for i in massdata:
                print(i)

    def get_names_players(self):
        pass

    def get_spawns(self):
        pass

    '''
    Print out all fleet information
    Give players choices
    wait for players to choose what to do
    Continue on with simulation
    '''

    def update_fleet_information(self):
        pass

    def make_new_ship_spec(self) -> dict:
        import ast
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
                        "Shipfolder Name", "HP", "Target Range", "Max Speed", "Signature", "Turret"))
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
        setanchormsg = "%s is being requested to select an anchor..." % players.name
        self.message_to_all_players(setanchormsg)
        singleplayerfleets.choosenewanchor()

    def message_to_all_players(self, setanchormsg):
        for playerstobemessage in self.playersplaying:
            self.listenersock.sendto(setanchormsg.encode("utf-8"),
                                     (playerstobemessage.address, int(playerstobemessage.port)))

    # We list the ships and the ship object addresses, because Sajuuk couldn't think of a quicker way to deal with unique ids.
    # Bare in mind, that there is a list of all ships in the world.  This list is not updated ever.
    def listofvalidprimaries(self):
        # we want player,distance,shiptype
        count = 0
        listofships = ""
        for players in self.playersplaying:
            for singleplayerfleets in players.owned_fleets:
                for individualships in singleplayerfleets.ships:
                    # print("%s %s %s %s %s" %(str(count), individualships.name,str(individualships.loc.x),str(individualships.loc.y),str(individualships.loc.z)))
                    listofships += "%s %s %s %s %s %s %s\n" % (
                    str(count), individualships.name[:-1], players.name, str(individualships.loc.x),
                    str(individualships.loc.y), str(individualships.loc.z), str(hex(id(individualships))))
        return listofships


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
            if state == 2:
                print("Combat Ended!\n")
            else:
                print("Error! :o \n")
            state = 0



        if menu_state == '3':
            break
