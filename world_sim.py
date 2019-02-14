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

    def shipcollection(self):
        pass
    def worldstate(self,state):
        if state == 0:
            print("collecting players and IPs")
            self.collect_ip_players()
            if len(self.playersplaying) == self.Howmanyplayers:
                state = 1


        if state == 1:
            print("%-30s %-20s %-50s" % ("Player Name","Address","Owned Fleets"))
            for i in range(0,len(self.playersplaying)):
                ownedshipslist = ""
                for j in range(0,len(self.playersplaying[i].owned_fleets)):
                    ownedshipslist = ownedshipslist + "," + self.playersplaying[i].owned_fleets[j]
                print("%-30s %-20s %-50s" % (self.playersplaying[i].name, self.playersplaying[i].address[0], str(ownedshipslist)))


            self.shipcollection()
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


class players():
    def __init__(self,name,addr):
        self.address = addr
        self.owned_fleets = []
        self.name = name
        print("\nMade player! Name " + self.name + " address " + self.address)


if __name__=="__main__":
    main_world = world()

    small_autocannon = weaponsystems.turret(100, 80, 90, "Small Autocannon", 8)
    FleetRed = fleet("Red",40)
    FleetBlue = fleet("Blue",50)


    state = 0


    while(True):
        state = main_world.worldstate(state)





