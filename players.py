import fleet
import weaponsystems


class players():
    def __init__(self, name, addr, port):
        self.address = addr.split(',')
        self.address = self.address[0][2:-1]
        self.owned_fleets = []
        self.name = name
        self.port = port
        print("\nMade player! Name " + self.name + " address " + self.address)

    def add_fleet(self, fleet: fleet.Fleet):
        self.owned_fleets.append(fleet)

    def populatefleet(self, fleetname):  # Output is a populated fleet

        new_fleet = fleet.Fleet(str(self.name) + " " + str(fleetname))

        fleetfile = open(str(fleetname), 'r')  # Read fleet file
        lines = fleetfile.readlines()

        # 2nd line is number of fleets
        for i in range(0, int(lines[1])):
            parsed_fleet = lines[i + 2].split(" ")
            for j in range(0, int(parsed_fleet[1])):  # pass
                new_fleet.add_ship_to_fleet(self.parse_ship_and_into_fleet(new_fleet, parsed_fleet))
            # should be put into its own fleet somewhere
        # 3rd+ are fleets

        # make a ship
        # generate ship
        return new_fleet

    def parse_ship_and_into_fleet(self, new_fleet, parsed_fleet):
        from Ship import ship
        import Ship.capacitor
        import Ship.ship_health

        shipfile = open(parsed_fleet[0].replace('.fleet', '.ship'), 'r')
        shiplines = shipfile.readlines()
        for i in range(len(shiplines)):
            shiplines[i] = shiplines[i].rstrip('\n')


        shield = Ship.ship_health.Shield(250, [50, 45, 40, 35], 0.1, 100)
        armor = Ship.ship_health.Armor(500, [30, 25, 20, 15])
        hull = Ship.ship_health.Hull(1000, [80, 75, 70, 65])
        capacitor = Ship.capacitor.capacitor(1000, 100, 0.2)
        name, hitpoints, targettingrange, speed, inertia, signature, weapon = map(str, shiplines)
        parsed_weapon = weaponsystems.parse_weapon(weapon)
        ship = ship.ship(int(hitpoints), 50, int(targettingrange), int(speed), int(inertia), name, 0, 0, 0, new_fleet,
                         parsed_weapon, capacitor, shield, armor, hull)
        # hitpoints, damage, targettingrange, speed, inertia, name, x, y, z, fleet, weapons):

        return ship
# shipspecs.append(input("Name of - $ "))
# shipspecs.append(input("Hitpoints of Ship $ "))
# shipspecs.append(input("Targetting Range of Ship $ "))
# shipspecs.append(input("Speed of Ship $ "))
# shipspecs.append(input("Inertia of Ship $ "))
# shipspecs.append(input("Signature of Ship $ "))
