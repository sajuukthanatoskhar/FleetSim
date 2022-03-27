import fleet

class PlayerState:
    AllFleetCapitulated = 0
    FleetsActive = 1
    NotInBattleYet = 2

class Players_c():
    """
    Class for players, their owned fleets, their state based off of their Fleets' states and connection details
    """

    def __init__(self, name, addr, port):
        self.address = addr.split(',')
        self.address = self.address[0][2:-1]
        self.owned_fleets = []
        self.name = name
        self.port = port
        self.alliance = None
        self.player_state = PlayerState.FleetsActive
        print("\nMade player! Name " + self.name + " address " + self.address)

    def add_fleet(self, fleet: fleet.Fleet):
        """

        :param fleet:
        :return:
        """
        self.owned_fleets.append(fleet)

    def populatefleet(self, fleetname: str) -> fleet.Fleet:  # Output is a populated fleet
        """

        :param fleetname: normally a string
        :return: fleet.Fleet object
        """
        new_fleet = fleet.Fleet(str(self.name) + " " + str(fleetname))
        fleetfile = open(str(fleetname), 'r')  # Read fleet file
        lines = fleetfile.readlines()
        # 2nd line is number of fleets
        for i in range(0, int(lines[1])):
            parsed_fleet = lines[i + 2].split(" ")  # Form is ["Muninn", "10"]
            for j in range(0, int(parsed_fleet[1])):
                """ 
                This gets the amount of ships into fleet
                """
                new_fleet.add_ship_to_fleet(self.parse_ship_and_into_fleet(parsed_fleet))
            # should be put into its own fleet somewhere
        # 3rd+ are fleets
        # make a ship
        # generate ship
        return new_fleet

    def parse_ship_and_into_fleet(self, parsed_fleet: fleet.Fleet):
        """
        Creates a ship object that is parsed from a json
        :param parsed_fleet:
        :return:
        """
        from Shipfolder import ship_f
        import json
        ship_dict = dict
        with open(parsed_fleet[0].replace('.fleet', '.ship'), 'r') as shipfile:
            ship_dict = json.load(shipfile)

        return ship_f.Ship(ship_dict)  # todo: problem?
