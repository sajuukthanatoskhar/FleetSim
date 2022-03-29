import pytest
from world_config import FleetStates,WorldStates, MenuMessages

@pytest.fixture
def worldsimulator_startup():
    return None

def test_end_of_combat(worldsimulator_startup):
    state = WorldStates.end_of_fight
    print(MenuMessages.menu_fleetcombat[f'{state}'])
    state = 0