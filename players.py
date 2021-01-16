import fleet


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

    def populatefleet(self, fleetname: str) -> fleet.Fleet:  # Output is a populated fleet
        new_fleet = fleet.Fleet(str(self.name) + " " + str(fleetname))
        fleetfile = open(str(fleetname), 'r')  # Read fleet file
        lines = fleetfile.readlines()
        # 2nd line is number of fleets


        for i in range(0, int(lines[1])):
            parsed_fleet = lines[i + 2].split(" ")  # Form is ["Muninn", "10"]
            for j in range(0, int(parsed_fleet[1])):
                """ This gets the amount of ships into fleet
                """
                new_fleet.add_ship_to_fleet(self.parse_ship_and_into_fleet(parsed_fleet))
            # should be put into its own fleet somewhere
        # 3rd+ are fleets

        # make a ship
        # generate ship
        return new_fleet

    def parse_ship_and_into_fleet(self, parsed_fleet):
        from Ship import ship
        import json
        ship_dict = dict
        with open(parsed_fleet[0].replace('.fleet', '.ship'), 'r') as shipfile:
            ship_dict = json.load(shipfile)

        #ship_dict['weapons'] = weaponsystems.parse_weapon(ship_dict['weapons'])
        ship = ship.ship(ship_dict)  # todo: problem
        return ship
