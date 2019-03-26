from fleet import *
import socket
from UDP_Server_Client.Server_Client import *

class world():
    def __init__(self):
        self.UDP_port_no = 6789
        self.Sender_Port_No = 6790
        self.UDP_IP_Address = "127.0.0.1"
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversock.bind(("", self.UDP_port_no))  # We are listening on 6789
        self.remoteip = "192.168.178.22"
        self.listenersock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Howmanyplayers = 1

        self.fleets = []
        self.ships = []
        self.playersplaying = []
        self.fleet_capitulation_status = 0 #0 is still active fleet, 1 is dead fleet
    '''All fleets will move/anchor '''
    def anchor_movephase(self):
        for i in range(0,len(self.fleets)):
            i.anchorup()

    '''Process all fleets attacking'''
    def attack_phase(self):
        # for i in range(0, len(self.fleets)):
        #     i.attack_other_fleet()
        pass
    '''Process all ships below <0 hull/hp'''
    def destroyed_ships_processing(self):
        pass

    def present_fleetchoices(self):
        pass

    def ship_allocation(self):
        for i in self.playersplaying:
            choice = -1
            while(choice != -2):
                fleetchoices= self.view("fleet")

                Fleetstring = ""

                for j in range(0,len(fleetchoices)):
                    Fleetstring = str(j) + ". " + fleetchoices[j] + "\n"


                message = "\nPlayer, which fleet do you want?  If you don't want to add a fleet, do -1"
                message = Fleetstring + message
                self.listenersock.sendto(message.encode("utf-8"),(i.address,int(i.port)))
                data,address = self.serversock.recvfrom(1024)
                #if choice.isdigit() & int(choice) > -1 & int(choice) < len(fleetchoices):
                choice = int(data)
                print(data)
                if int(choice) > -1 and int(choice) < len(fleetchoices):
                    i.add_fleet(fleetchoices[choice])
                elif int(choice) == -2:
                    choice = -2

                #todo: after fleets have been chosen by all players, we move on to battle











    def worldstate(self,state):
        if state == 0:
            print("collecting players and IPs")
            self.collect_ip_players()
            if len(self.playersplaying) == self.Howmanyplayers:
                state = 1


        if state == 1:
            count = 0
            print("\nAllocating Fleets to players, please wait")
            for player in self.playersplaying:
                print(player.name)
                playerreceived = player.name
                print(player.name + " " + player.address + " " + player.port)
                self.listenersock.sendto(playerreceived.encode("utf-8"), (player.address, int(player.port)))
                data,addr = self.serversock.recvfrom(1024)
                data = data.decode('utf-8')
                if data == "ok":
                    count = 1 + count
            print("count = %s"%str(count))
            state = 2





        if state == 2:
            statechoice = -1
            while(statechoice == -1):
                print("%-30s %-20s %-50s" % ("Player Name","Address","Owned Fleets\n"))
                for i in range(0,len(self.playersplaying)):
                    ownedshipslist = ""
                    for j in range(0,len(self.playersplaying[i].owned_fleets)):
                        ownedshipslist = ownedshipslist + "," + self.playersplaying[i].owned_fleets[j]
                    print("%-30s %-20s %-50s" % (self.playersplaying[i].name, self.playersplaying[i].address, str(ownedshipslist)))

                self.ship_allocation()  # todo players need to get fleets.
                statechoice = 0
                state = 3
        if state == 3:
            #todo:  at this point, fleets aren't a thing yet, they need to be loaded into existence.
            #todo: then after the loading, they need to be placed on the field, given an anchor

            #todo: we do battle ehre, all players should have their fleets at this point.   The word needs to set up a battle arena .
            #todo: need anchor for
            while(True):
                print("Fleet Fighting Mode")

        return state




    def collect_ip_players(self):
        data, addr = self.serversock.recvfrom(1024)
        data = data.decode("utf-8")
        if "fleetplayer" in data:
            #format will be 'fleetplayer,name'
            massdata = data.split(',')
            self.playersplaying.append(players(str(massdata[1]),str(addr),str(massdata[2])))
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

    def buildfleet(self):
        state = -1
        while(True):
            state = input("1. Design Fleet\n2. Design Ships\n3. Design Weapon"
                          "\n4. View Fleets made\n5. View Ships made\n6. View Turrets\n7. Go back")
            if state == '1':
                fleetname = input("Name of Fleet? $ ")
                shipsinfleet = []
                numshipsinfleet = []
                shiplist = self.view("ship")
                choice = -1
                while(choice == -1):
                    choice = -1

                    while(int(choice) <= -1 or int(choice) >= len(shiplist)-1):
                        print("%15s\t%10s\t%10s\t%10s\t%10s\t%10s" % ("Ship Name", "HP", "Target Range", "Max Speed", "Signature", "Turret"))
                        for i in shiplist:
                            filet = open(i,'r')
                            content = filet.readlines()
                            #todo print out optimal falloff and dps
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
                            while(True):
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





                f = open(fleetname + ".fleet","w+")
                f.write(str(fleetname))

                if len(shipsinfleet) == len(numshipsinfleet):
                    f.write("\n" + str(len(shipsinfleet)))
                    for i in range(0,len(shipsinfleet)):
                        f.write("\n" + str(shipsinfleet[i]) + " " + str(numshipsinfleet[i]))


                f.close
            if state == '2':
                shipspecs = []
                shipspecs.append(input("Name of - $ "))
                shipspecs.append(input("Hitpoints of Ship $ "))
                shipspecs.append(input("Targetting Range of Ship $ "))
                shipspecs.append(input("Speed of Ship $ "))
                shipspecs.append(input("Inertia of Ship $ "))
                shipspecs.append(input("Signature of Ship $ "))
                print("\nChoose Turret:")
                turretlist = self.view("turret")
                choice = -1
                while(int(choice) <= -1 or int(choice) >= len(turretlist)-1):
                    print("%20s\t%10s\t%10s\t%10s\t%10s" % ("Turret System Name", "Optimal Range","Falloff","Damage Per Second","WSA"))
                    for i in turretlist:
                        filet = open(i,'r')
                        content = filet.readlines()
                        print("%20s\t%10s\t%10s\t%10s\t%10s"% (content[0][:-1],content[1][:-1],content[2][:-1],content[3][:-1],content[4][:-1]))

                    choice = int(input("Choose a turret type"))
                    if (choice <= -1 or choice >= len(turretlist)):
                        print("\nError:Choose a valid number!\n")
                    else:
                        shipspecs.append(turretlist[choice])

                #todo: Add in confirmation before write




                f = open(shipspecs[0] + ".ship","w+")
                for i in range(0,len(shipspecs)):
                    f.write(shipspecs[i] + "\n")
                f.close()

            if state == '3':
                shipspecs = []
                shipspecs.append(input("Name of Turret"))
                shipspecs.append(input("Optimal of Turret"))
                shipspecs.append(input("Falloff of Turret"))
                shipspecs.append(input("DPS of Turret"))
                shipspecs.append(input("WSA of Turret"))
                f = open(shipspecs[0] + ".turret","w+")
                #Design weapons
                for i in range(0,len(shipspecs)):
                    f.write(shipspecs[i] + "\n")

                f.close()

            if state == '4':
                self.view('fleet')
            if state == '5':
                self.view('ship')
            if state == '6':
                self.view('turret')

            if state == '7':
                return -1

    def read_ship(self, shipfile):
        pass

    def view(self, param):
        availabilitylist = [] # for shipcreation
        count = 0
        print('\n***********************************************************\nSaved %ss\n-----------'%param)
        for i in os.listdir():
            if '.' + param in i:

                availabilitylist.append(i)
                print(str(count) + ". " + i)
                count = count + 1
        print('******************************************************************')
        return availabilitylist

    def give_fleets(self):
        #todo players will receive a signal signalling what fleets there are, there should be a summary of things maybe
        pass


class players():
    def __init__(self,name,addr,port):
        self.address = addr.split(',')
        self.address = self.address[0][2:-1]
        self.owned_fleets = []
        self.name = name
        self.port = port
        print("\nMade player! Name " + self.name + " address " + self.address)

    def add_fleet(self, fleet):
        self.owned_fleets.append(fleet)




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


if __name__=="__main__":
    main_world = world()

    #small_autocannon = weaponsystems.turret(100, 80, 90, "Small Autocannon", 8,40)
    #FleetRed = fleet("Red",40)
    #FleetBlue = fleet("Blue",50)

    # for i in range(0,10,1):
    #     FleetRed.ships.append(ship(800,2,60,5,1,"Thanatos_"+str(i),random.randint(30,150),random.randint(30,150),20,FleetRed,small_autocannon))
    #     FleetBlue.ships.append(ship(500,2,70,2,1,"Nyx_" +str(i),50,150,20,FleetBlue,small_autocannon))



    state = 0

    printMMD()
    while(True):

        menu_state = input("\n\nTEST Alliance Fleet Simulator \n1.\tMake fleet?\n2.\tBattlefleets?\n3.\tQuit\n\nMake your choice, Fleet Commander of Test... \n $ ")
        if menu_state == '1':
            main_world.buildfleet()

        if (menu_state == '2'):
            while(True):
                state = main_world.worldstate(state)
        if menu_state == '3':
            break




