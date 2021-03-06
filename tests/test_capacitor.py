from unittest import TestCase

import Shipfolder.capacitor

tested_capacitor_dict = {
            "capacitorCapacity": 500,
            "max_capacitor": 500,
            "rechargeRate": 10000,
            "energyWarfareResistance": 0.5
        }
# 500, 10, 0.5)
tested_capacitor = Shipfolder.capacitor.capacitor(tested_capacitor_dict)

class TestCapacitor(TestCase):
    def test_modify_capacitor(self):
        tested_capacitor.capacitor_level = tested_capacitor.max_capacitor
        tested_capacitor.modify_capacitor(500, rep=False)

        self.assertEqual(tested_capacitor.modify_capacitor(250, rep=False)[0], Shipfolder.capacitor.status['damaged'])

    def test_recharge_tick(self):
        tested_capacitor.capacitor_level = 250
        self.assertAlmostEqual(tested_capacitor.recharge_tick(), 103.55, 2)



    def test_capacitor_damage(self):
        tested_capacitor.capacitor_level = tested_capacitor.max_capacitor
        self.assertEqual(tested_capacitor.capacitor_damage(500)[0], 250)

    def test_reflected_capacitor_damage(self):
        tested_capacitor.capacitor_level = tested_capacitor.max_capacitor
        self.assertAlmostEqual(tested_capacitor.capacitor_damage(500)[0], 250, 2)