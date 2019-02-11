from fleet import *
import socket

class world():
    def __init__(self):
        self.fleets = []
        self.ships = []
        self.playersplaying = []
        self.fleet_capitulation_status = 0 #0 is still active fleet, 1 is dead fleet
    '''All fleets will move/anchor '''
    def anchor_movephase(self):
        pass

    '''Process all fleets attacking'''
    def attack_phase(self):
        pass

    '''Process all ships below <0 hull/hp'''
    def destroyed_ships_processing(self):
        pass


    def collect_ip_players(self):
        pass

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
    def __init__(self):
        self.socket = ""
        self.owned_fleets = []
        self.name = ""