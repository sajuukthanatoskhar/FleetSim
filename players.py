import fleet
import weaponsystems
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

    def populatefleet(self,fleetname): #Output is a populated fleet

        new_fleet = fleet.fleet(str(self.name) + " " + str(fleetname))

        fleetfile = open(str(fleetname),'r') #Read fleet file
        lines = fleetfile.readlines()

        #2nd line is number of fleets
        for i in range(0,int(lines[1])):
            parsed_fleet = lines[i+2].split(" ")
            for j in range(0,int(parsed_fleet[1])): #pass
                new_fleet.add_ship_to_fleet(self.parse_ship_and_into_fleet(new_fleet,parsed_fleet))
            #should be put into its own fleet somewhere
        #3rd+ are fleets


        #make a ship
        #generate ship
        return new_fleet

    def parse_ship_and_into_fleet(self, new_fleet,parsed_fleet):
        import ship
        shipfile = open(parsed_fleet[0].replace('.fleet','.ship'),'r')
        shiplines = shipfile.readlines()
        name, hitpoints, targettingrange, speed, inertia, signature,weapon = map(str, shiplines)
        parsed_weapon = weaponsystems.parse_weapon(weapon)
        ship = ship.ship(int(hitpoints),50,int(targettingrange),int(speed),int(inertia),name,0,0,0,new_fleet,parsed_weapon)
        # hitpoints, damage, targettingrange, speed, inertia, name, x, y, z, fleet, weapons):

        return ship
# shipspecs.append(input("Name of - $ "))
# shipspecs.append(input("Hitpoints of Ship $ "))
# shipspecs.append(input("Targetting Range of Ship $ "))
# shipspecs.append(input("Speed of Ship $ "))
# shipspecs.append(input("Inertia of Ship $ "))
# shipspecs.append(input("Signature of Ship $ "))
