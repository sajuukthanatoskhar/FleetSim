
class WorldStates():
    preload_ips_players = 0 # collecting players and IPs
    player_allocation = 1 # Allocating Fleets to players, please wait
    initialise_fleets = 2
    Fleet_Combat_State = 3
    error = -1

    end_of_fight = 4



class FleetStates():
    fleet_capitulated = 0
    fleet_non_combat = 3
    fleet_combat_effective = 1

class CommunicationResponses:
    PlayerClient_To_Server_ExistenceACK = "ok"

class WorldConfig():
    time_dilation_factor = 0.5

class MenuMessages:
    menu_fleetcombat = {
        f'{WorldStates.end_of_fight}' : "Combat Ended!\n",
        f'{WorldStates.error}' : "Error! :o \n",
        }