from unittest import TestCase
import weaponsystems
import ship


BlueFleet = ship.fleet("Blue Fleet")
RedFleet = ship.fleet("Red Fleet")

small_autocannon = weaponsystems.turret(50, 50, 50, "Small Autocannon",8)
redship = ship.ship(100,50,50,50,1,"Test Dummy 1",50,50,50,RedFleet,small_autocannon)
blueship = ship.ship(100,50,50,50,1,"Test Dummy 2",100,50,50,BlueFleet,small_autocannon)

class TestTurret(TestCase):
    def test_fire_weapon(self):
        assert small_autocannon.dps == 50
    def test_checkrange(self):
        assert redship.calc_distance(blueship) == redship.weapon.optimal
    def test_withinrange(self):
        assert redship.calc_distance(blueship) <= redship.weapon.optimal
    def test_chance(self):
        print(redship.calc_weapon_avg_dps_mod(blueship))