from unittest import TestCase
import fleet
import players
import pytest


@pytest.fixture
def setup_test_fleet_and_player():
    tested_fleet = fleet.Fleet("TEST Fleet Please Ignore")
    tested_player = players.players("Sajuuk", "127.0.0.1", "7398")
    return tested_fleet, tested_player

@pytest.fixture
def setup_player_and_connected_fleet():
    tested_fleet = fleet.Fleet("TEST Fleet Please Ignore")
    tested_player = players.players("Sajuuk", "127.0.0.1\n", "7398")
    tested_player.add_fleet(tested_fleet)
    return tested_fleet, tested_player

def test_player_attributes(setup_test_fleet_and_player):
    tested_player = setup_test_fleet_and_player[1]
    errors = []
    if tested_player.name != "Sajuuk":
        errors.append("Incorrect Player name : {} should be Sajuuk".format(tested_player.name))
    if tested_player.address != "127.0.0.1":
        errors.append("Incorrect Address value : {} should be 127.0.0.1".format(tested_player.address))
    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))

def test_add_fleet(setup_test_fleet_and_player):
    tested_player = setup_test_fleet_and_player[1]
    tested_fleet = setup_test_fleet_and_player[0]
    tested_player.add_fleet(tested_fleet)
    assert (len(tested_player.owned_fleets) == 1 and tested_player.owned_fleets[0].name == tested_fleet.name)

def test_populatefleet(setup_player_and_connected_fleet):
    tested_players_fleet = setup_player_and_connected_fleet[1].populatefleet("Muninn.fleet")
    errors = []
    if tested_players_fleet.ships[0].name is not "Muninn":
        errors.append("Incorrect name :" + tested_players_fleet.ships[0].name)
    assert not errors, "Errors occurred occured: \n{}".format("\n".join(errors))