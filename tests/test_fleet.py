import pytest
import fleet
import Ship.ship as ship
import Ship.capacitor as capacitor
import Ship.ship_health as shiphealth

tested_ship = ship.ship(150, 150, 100000, 200, 1.5, "TestShip",
                        0, 0, 0, None, "Small Autocannon.turret",
                        capacitor.capacitor(2000, 200, 0.1),
                        shiphealth.Shield(1000, [60, 40, 40, 20], 0.1, 100),
                        shiphealth.Armor(1000, [50, 50, 25, 0]),
                        shiphealth.Hull(500, [0, 0, 0, 0])
                        )


@pytest.fixture
def make_fleet():
    return fleet.Fleet("Test")


def test_fleet_attr(make_fleet):
    errors = []
    if make_fleet.ships:
        errors.append("Error: There should be no ships, has {}".format(len(make_fleet.ships)))
    if make_fleet.name != "Test":
        errors.append("Error: Name should be 'Test', is {}".format(make_fleet.name))
    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_add_ship_to_fleet(make_fleet):
    errors = []

    tested_fleet = make_fleet
    tested_fleet.add_ship_to_fleet(tested_ship)

    if len(tested_fleet.ships) != 1:
        errors.append("Error: There should only be 1 ship in the fleet")

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_remove_ship(make_fleet):
    """
    only removes a ship that was just put in, but what about a random ship due to low health?
    :param make_fleet:
    :return:
    """
    errors = []
    tested_fleet = make_fleet
    tested_fleet.ships = []
    tested_fleet.add_ship_to_fleet(tested_ship)
    tested_fleet.remove_ship(tested_fleet.ships[0], "Dead")

    assert len(tested_fleet.ships) == 0, "Error: Should not have any ships in the ships list of fleet"


def test_listallfleetmembers(make_fleet):
    errors = []
    tested_fleet = make_fleet
    tested_fleet.ships = []
    tested_fleet.add_ship_to_fleet(tested_ship)
    tested_fleet.add_ship_to_fleet(tested_ship)
    tested_fleet.add_ship_to_fleet(tested_ship)
    tested_fleet.add_ship_to_fleet(tested_ship)
    tested_fleet.add_ship_to_fleet(tested_ship)


    assert len(tested_fleet.ships) == 5, "Error: There should be 5 ships in the fleet"


def test_range_from_anchor():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_default_fleet_activity():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_set_anchor():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_anchor_move_to_target():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_anchorup():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_chooseprimary():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_fleet_choose_primary_now():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_fleet_attack_procedure():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_attack_primary():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_attack_other_fleet():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_choosenewanchor():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_checkenemyfleetdead():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))


def test_printstats():
    errors = []

    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))
