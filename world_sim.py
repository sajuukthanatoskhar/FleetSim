from fleet import *
import socket
from UDP_Server_Client.Server_Client import *

class world():
    def __init__(self):
        self.UDP_port_no = 6789
        self.Sender_Port_No = 6790
        self.UDP_IP_Address = "127.0.0.1"
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversock.bind(("", self.UDP_port_no))
        self.remoteip = "192.168.178.22"
        self.listenersock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Howmanyplayers = 2



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

    def ship_allocation(self):
        pass



    def worldstate(self,state):
        if state == 0:
            print("collecting players and IPs")
            self.collect_ip_players()
            if len(self.playersplaying) == self.Howmanyplayers:
                state = 1


        if state == 1:
            self.give_fleets()



        if state == 2:
            print("%-30s %-20s %-50s" % ("Player Name","Address","Owned Fleets"))
            for i in range(0,len(self.playersplaying)):
                ownedshipslist = ""
                for j in range(0,len(self.playersplaying[i].owned_fleets)):
                    ownedshipslist = ownedshipslist + "," + self.playersplaying[i].owned_fleets[j]
                print("%-30s %-20s %-50s" % (self.playersplaying[i].name, self.playersplaying[i].address[0], str(ownedshipslist)))


            self.ship_allocation()
            #wait for players
            #collect ips

        return state




    def collect_ip_players(self):
        data, addr = self.serversock.recvfrom(1024)
        data = data.decode("utf-8")
        if "fleetplayer" in data:
            #format will be 'fleetplayer,name'
            massdata = data.split(',')
            self.playersplaying.append(players(str(massdata[1]),str(addr)))



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


    def FleetGeneration(self):
        while(True):
            state = input("Fleets or Ships?")
            while(state == 0):
                pass
            while(state == 1):
                name_ship = input("\nName of Ship?")
                ship_file = open(name_ship+".shfit","w+")
                ship_hp = input("\nHP of ship?")
                ship_dps = input("\nDPS of ship?")
                ship_speed = input("\nName of Ship?")
                ship_targetting = input("\ntargetting range")
                ship_signature = input("\nshipsig?")
                ship_input("\nName of Ship?")
            while(state == 2):
                return 0

    def buildfleet(self):
        state = -1
        while(True):
            state = input("1. Design Fleet\n2. Design Ships\n3. Design Weapon"
                          "\n4. View Fleets made\n5. View Ships made\n6. View Turrets\n7. Go back")
            if state == '1':
                fleetname = input("Name of Fleet? $ ")
                f = open(fleetname + ".fleet","w+")
                f.write("fname\t" + str(fleetname))
                f.close
            if state == '2':
                shipspecs = []
                shipspecs.append(input("Name of Ship $ "))
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


class players():
    def __init__(self,name,addr):
        self.address = addr
        self.owned_fleets = []
        self.name = name
        print("\nMade player! Name " + self.name + " address " + self.address)


if __name__=="__main__":
    main_world = world()

    small_autocannon = weaponsystems.turret(100, 80, 90, "Small Autocannon", 8,40)
    FleetRed = fleet("Red",40)
    FleetBlue = fleet("Blue",50)

    for i in range(0,10,1):
        FleetRed.ships.append(ship(800,2,60,5,1,"Thanatos_"+str(i),random.randint(30,150),random.randint(30,150),20,FleetRed,small_autocannon))
        FleetBlue.ships.append(ship(500,2,70,2,1,"Nyx_" +str(i),50,150,20,FleetBlue,small_autocannon))



    state = 0


    while(True):
        menu_state = input("1.\tMake fleet?\n2.\tBattlefleets?\n3.\tQuit")
        if menu_state == '1':
            main_world.buildfleet()

        if (menu_state == '2'):
            while(True):
                state = main_world.worldstate(state)
        if menu_state == '3':
            break




