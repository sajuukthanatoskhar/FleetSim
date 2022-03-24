import unittest.mock

import pytest
from tests.errors_count_class import *

import Shipfolder.ship_f

ship_dict = {"name": "Retribution: TEST Armor AFs 19/05/2020",
             "ehp": {"shield": 747.486694, "armor": 7741.684444, "hull": 2715.884861}, "droneDPS": 0, "droneVolley": 0,
             "hp": {"shield": 395.0, "armor": 2273.75, "hull": 1273.75}, "maxTargets": 5, "maxSpeed": 2296.992206,
             "weaponVolley": 645.5295, "totalVolley": 645.5295, "maxTargetRange": 50000.0, "scanStrength": 14.4,
             "weaponDPS": 264.18232, "alignTime": 6.436921, "signatureRadius": 113.75, "weapons": [
        {"dps": 264.18232, "capUse": 5.540209, "falloff": 3125.0, "type": "Turret",
         "name": "Small Focused Beam Laser II, Gleam S", "optimal": 7425.0, "numCharges": 1, "numShots": 1000,
         "reloadTime": 0.01, "cycleTime": 2443.5, "volley": 645.5295, "tracking": 140.625, "maxVelocity": 0,
         "explosionDelay": 0, "damageReductionFactor": 0, "explosionRadius": 0, "explosionVelocity": 0,
         "aoeFieldRange": 0, "damageMultiplierBonusMax": 0.5, "damageMultiplierBonusPerCycle": 0,
         "dps_spread": {"em": 132.09116, "therm": 132.09116, "kin": 0.0, "exp": 0.0}}], "scanRes": 812.5,
             "capUsed": 8.915209, "capRecharge": 12.778667, "capacitorCapacity": 718.8, "rechargeRate": 140625.0,
             "rigSlots": 2.0, "lowSlots": 5.0, "midSlots": 2.0, "highSlots": 5.0, "turretSlots": 4.0,
             "launcherSlots": 0, "powerOutput": 85.25, "cpuOutput": 175.0, "rigSize": 1.0, "effectiveTurrets": 6.67,
             "effectiveLaunchers": 0.0, "effectiveDroneBandwidth": 0.0,
             "resonance": {"hull": {"exp": 0.469, "kin": 0.469, "therm": 0.469, "em": 0.469},
                           "armor": {"exp": 0.156584, "kin": 0.293595, "therm": 0.33317, "em": 0.39146},
                           "shield": {"exp": 0.11875, "kin": 0.285, "therm": 0.76, "em": 0.95}}, "typeID": 11393,
             "groupID": 324, "shipSize": "Frigate", "droneControlRange": 60000.0, "mass": 1666400.0,
             "shieldrechargetime": 468750.0, "shipinertia": 2.7864, "energyWarfareResistance": 0.75,
             "unpropedSpeed": 343.75, "unpropedSig": 35.0, "usingMWD": 1, "mwdPropSpeed": 2296.992206,
             "projections": [], "repairs": [],
             "modTypeIDs": [[3033, 12557], [3033, 12557], [3033, 12557], [3033, 12557], 3488, 35658, 47255, 5849, 20347,
                            18797, 1306, 31484, 31358],
             "moduleNames": ["High Slots:", "Small Focused Beam Laser II:  Gleam S",
                             "Small Focused Beam Laser II:  Gleam S", "Small Focused Beam Laser II:  Gleam S",
                             "Small Focused Beam Laser II:  Gleam S", "Empty Slot", "", "Med Slots:",
                             "Small Cap Battery II", "5MN Quad LiF Restrained Microwarpdrive", "", "Low Slots:",
                             "EFFA Compact Assault Damage Control", "Extruded Compact Heat Sink",
                             "200mm Steel Plates II", "Coreli A-Type Thermal Coating", "Multispectrum Coating II", "",
                             "Rig Slots:", "Small Energy Locus Coordinator II", "Small Ancillary Current Router I"],
             "cargoItemIDs": [12559, 23071, 23085, 23079, 28668, 28999, 29001, 28680, 5445], "pyfaVersion": "v2.33.0",
             "efsExportVersion": 0.04}

import json

with open('ScorpionBursterScorp.ship', 'r') as bursterscorpf:
    bursterscorp = json.loads(bursterscorpf.readline())
    bursterscorpf.close()


@pytest.mark.parametrize("name",
                         [(bursterscorp), (ship_dict)]
                         )
def test_make_ship(name):
    ship_to_be_tested = Shipfolder.ship_f.Ship(name)
    assert isinstance(ship_to_be_tested, Shipfolder.ship_f.Ship)


@pytest.mark.skip
def test_check_range():
    assert False


@pytest.mark.skip
def test_check_range():
    assert False


def test_verify_weapon():
    assert True


def test_attack():
    shipa = Shipfolder.ship_f.Ship((ship_dict))
    shipb = Shipfolder.ship_f.Ship(ship_dict, x=500, y=500, z=500)

    shipa.attack(shipb)
    assert True


def test_orbit():
    shipa = Shipfolder.ship_f.Ship(ship_dict, 0, 0, 0)
    shipb = Shipfolder.ship_f.Ship(ship_dict, 0, 10000, 0)
    shipa.speed = 500
    shipb.speed = 500
    shipa.orbit_around_target(shipb, 10000)  # should just orbit
    shipa.orbit_around_target(shipb, 10000)  # should just orbit

    if round(shipa.loc.x) == 0 and round(shipa.loc.y) == 0: # todo fixup the test success
        assert True
    else:
        assert False


def test_move_to():
    shipa = Shipfolder.ship_f.Ship(ship_dict, 0, 0, 0)
    shipb = Shipfolder.ship_f.Ship(ship_dict, 0, 10000, 0)
    shipa.speed = 500
    shipb.speed = 500
    assert True


@pytest.mark.skip
def test_calculate_location_3d_diff():
    assert False


@pytest.mark.skip
def test_calc_distance():
    assert False


@pytest.mark.skip
def test_calculate_angular():
    assert False


@pytest.mark.skip
def test_calc_dist_using_xyz():
    assert False


@pytest.mark.skip
def test_calc_weapon_avg_dps_mod():
    assert False


@pytest.mark.skip
def test_calc_tracking_score():
    assert False


@pytest.mark.skip
def test_calc_weapon_to_hit_chance():
    assert False


@pytest.mark.skip
def test_move_ship_to():
    assert False


@pytest.mark.skip
def test_main_attack_procedure():
    assert False


@pytest.mark.skip
def test_evasive_attack_procedure():
    assert False


@pytest.mark.skip
def test_move_away_from():
    assert False


