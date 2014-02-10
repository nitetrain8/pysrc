__author__ = 'Nathan Starkweather'
'''

Created by: Nathan Starkweather
Created on: 02/09/2014
Created in: PyCharm Community Edition


'''


# noinspection PyUnresolvedReferences
from foods import Food, foods_from_dict


def make_foods():
    Yogurt = Food("Greek Yogurt",
                  serving_size=227,
                  serving_cal=120,
                  protein=22,
                  fat=7)
    Cream = Food("Heavy Cream",
                 serving_size=15,
                 serving_cal=50,
                 protein=0,
                 carbs=0.5,
                 fat=5)

    Egg = Food("Large Egg",
               serving_size=54,
               serving_cal=73.5,
               protein=6.29,
               carbs=0.39,
               fat=4.97)
    Milk = Food("Milk 1%",
                240,
                130,
                10,
                16,
                2.5)
    IFWhey = Food("IForce Protean Vanilla Cupcake Batter",
                  34,
                  120,
                  20,
                  6.5,
                  4.0)
    BrownSugar = Food("Dark Brown Sugar",
                      4,
                      15,
                      0,
                      4,
                      0)
    foods = foods_from_dict(locals())
    return foods
