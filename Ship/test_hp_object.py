from unittest import TestCase
import Ship.ship_health as ship_health

tested_ship_shield = ship_health.Shield(500, [25, 50, 75, 100], 0.1, recharge_time=10)
testing_weapon = ship_health.damage_types([100,100,100,100])

class TestShield(TestCase):
    def test_recharge_tick(self):
        tested_ship_shield.hp = 250
        self.assertAlmostEqual(103.55, tested_ship_shield.recharge_tick(), 2, "Shield Recharge Functions")


class TestHP_Object(TestCase):
    def test_modify_hp(self):
        tested_ship_shield.hp = tested_ship_shield.max_hp
        self.assertEqual(tested_ship_shield.modify_hp(100), 0)

    def test_be_attacked(self):
        tested_ship_shield.hp = tested_ship_shield.max_hp
        tested_ship_shield.be_attacked(testing_weapon)
        self.assertEqual(350, tested_ship_shield.hp)


class TestDamage_types(TestCase):
    def test_get_EM(self):
        self.assertEqual(testing_weapon.get_EM(), 100)

    def test_get_Thermal(self):
        self.assertEqual(testing_weapon.get_Thermal(), 100)

    def test_get_Kinetic(self):
        self.assertEqual(testing_weapon.get_Kinetic(), 100)

    def test_get_Explosive(self):
        self.assertEqual(testing_weapon.get_Explosive(), 100)
