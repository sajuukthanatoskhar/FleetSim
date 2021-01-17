import tkinter
from tkinter import *
from FleetSim.ShipCreator import *

class main_menu_window():
    def __init__(self,master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.make_ship = Button(master, text="Make Ship", command=self.make_ship)
        self.make_ship.pack()

        self.configure_fleet = Button(master, text="Configure fleets", command=self.make_fleet)
        self.configure_fleet.pack()

        self.battle_button = Button(master, text="Battle fleets", command=self.battlefleets)
        self.battle_button.pack()

        self.close_button = Button(master, text="Quit", command=master.quit)
        self.close_button.pack()

    def battlefleets(self):
        print("Battle!!!")

    def make_fleet(self):
        print("Make fleet")