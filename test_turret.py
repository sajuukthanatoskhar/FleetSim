from unittest import TestCase
import weaponsystems
import ship
import math
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

BlueFleet = ship.fleet("Blue Fleet",50)
RedFleet = ship.fleet("Red Fleet",50)

small_autocannon = weaponsystems.turret(50, 50, 50, "Small Autocannon",40)
redship = ship.ship(1000,50,50,50,1,"Test Dummy 1",99,50,50,RedFleet,small_autocannon)
blueship = ship.ship(1000,50,50,50,1,"Test Dummy 2",100,50,50,BlueFleet,small_autocannon)

class TestTurret(TestCase):
    def test_fire_weapon(self):
        assert small_autocannon.dps == 50
    def test_checkrange(self):
        assert redship.calc_distance(blueship) == redship.weapon.optimal
    def test_withinrange(self):
        assert redship.calc_distance(blueship) <= redship.weapon.optimal
    def calc_weap_dps(self):
        redship.attack(blueship)
    def test_guns(self):
        #need to do a fuckton fo tests
        #distance vs success vs damage
        distance = []
        chancesuccess = []
        damage = []
        for i in range(0,200,1): #todo: Extract distance from target, success and damage
            distance.append(redship.calc_distance(blueship))
            test,success = redship.calc_weapon_to_hit_chance(blueship)
            chancesuccess.append(test)
            lower,upper,avgdps = redship.calc_weapon_avg_dps_mod(blueship,test)
            damage.append(math.floor(redship.weapon.dps*avgdps))

            print("%s,%s,%s"% (distance[i],chancesuccess[i],damage[i]))
            redship.loc.translate_location()
            redship.loc.x += -1



            #damage comes from ship
            #distance to target is from ship
            #success is a return


            #move the ships in a certain pattern, a line is good

        # df = pd.DataFrame([distance,chancesuccess])
        # popt, pcov = curve_fit(func, distance, chancesuccess)
        # func(distance, *popt)
        # plt.plot(distance, func(distance, *popt), label="Fitted")
        # plt.show()
        pass

# def func(x,a,b,c,e,f):
#     return np.power(0.5,np.power((a*40000)/(b*c),2)+np.power(max(0,x-e)/f,2))
#     #     print(redship.calc_weapon_avg_dps_mod(blueship))