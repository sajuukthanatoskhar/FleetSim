from Ship.ship import location

def define_location() -> location:
    return


def test_distance_translation_no_old():
    '''

    :return:
    '''
    tested_location = location(1, 2, 3)
    assert tested_location.find_distance_for_translation() == 0

def test_distance_translation_with_old():
    tested_location = location(1, 2, 3)
    tested_location.translate_location()
    tested_location.x = 5
    tested_location.y = 6
    tested_location.z = 3
    import math
    assert tested_location.find_distance_for_translation() == math.sqrt(4**2+4**2+0)