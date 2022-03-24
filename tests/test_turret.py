import pytest
from tests.errors_count_class import *
import Shipfolder.weapon as weapon

testweapon = {"dps": 100, "capUse": 10, "falloff": 3000, "type": "Turret",
              "name": "Small Focused Beam Laser II, Gleam S", "optimal": 8000, "numCharges": 1, "numShots": 1000,
              "reloadTime": 10, "cycleTime": 5000, "volley": 500, "tracking": 100, "maxVelocity": 0,
              "explosionDelay": 0, "damageReductionFactor": 0, "explosionRadius": 0, "explosionVelocity": 0,
              "aoeFieldRange": 0, "damageMultiplierBonusMax": 0.5, "damageMultiplierBonusPerCycle": 0,
              "dps_spread": {"em": 25, "therm": 75, "kin": 0.0, "exp": 0.0}}


def test_weapon_general():
    test_weapon = weapon.Weapon(testweapon)
    error_hist = error_count()

    if test_weapon.cycleTime != 5000:
        error_hist.add_error("Incorrect cycle time")


def test_weapon_cycle():
    test_weapon = weapon.Weapon(testweapon)
    error_hist = error_count()



    assert error_hist.check_errors()
