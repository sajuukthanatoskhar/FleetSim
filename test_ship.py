from unittest import TestCase
from fleet import *
from ship import *

class TestShip(TestCase):

    RedFleet = fleet("Red",40)
    small_autocannon = weaponsystems.turret(100, 80, 90, "Small Autocannon", 8)
    ship1 = ship(50,50,50,50,1,"Red 1", 0, 0,0,RedFleet,small_autocannon)


    def test_check_range(self):
        pass


