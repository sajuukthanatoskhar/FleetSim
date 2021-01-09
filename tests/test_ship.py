import pytest

import Ship.ship

ship_dict = {
    "hitpoints": 500,
    "damage": 100,
    "targettingrange" : 100000,
    "signature": 50,
    "speed" : 400,
    "inertia" : 1,
    "name": "Test_Ship",
    "x" : 0,
    "y" : -1,
    "z" : 1,
    "fleet" : None,
    "weapons": None,
    "projections": None,
    "capacitor": {"capacitor_capacity": 5000,
                  "max_capacitor": 5000,
                  "time_to_recharge": 100,
                  "neut_resistance": 0.1},
    "shield": {"hp": 2500,
               "resistance": [75, 50, 25, 0],
               "shield_leak": 0.1,
               "recharge_time": 100},
    "armor": {"hp": 2500,
              "resistance": [50, 50, 25, 0]},
    "hull": {"hp": 2500,
             "resistance": [75, 85, 50, 25]}
}


def test_make_ship():
    ship_to_be_tested = Ship.ship.ship(ship_dict)
    assert isinstance(ship_to_be_tested, Ship.ship.ship)

@pytest.mark.skip
def test_check_range():
    assert False


@pytest.mark.skip
def test_check_range():
    assert False


@pytest.mark.skip
def test_attack():
    assert False


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
