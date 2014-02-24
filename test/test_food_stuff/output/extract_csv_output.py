"""

Created by: Nathan Starkweather
Created on: 02/22/2014
Created in: PyCharm Community Edition

Hold some python objects which should be replicated by the test functions.
Sometimes it is easier to build the test objects at runtime,
sometimes it is easier to write them in here.

Time will tell which is better.
"""
from collections import OrderedDict
from os.path import dirname, join, normpath

outputdir = dirname(__file__)
testdir = dirname(outputdir)
indir = join(testdir, "input")

indir = normpath(indir)
testdir = normpath(testdir)
outputdir = normpath(outputdir)

with open(join(indir, "extract_csv_good1.csv"), 'r') as f:
    csv_good_fnames1 = f.readline().rstrip('\n').split(',')
    csv_good_ftypes1 = f.readline().rstrip('\n').split(',')

    csv_good_attrvals1 = []
    for line in f:
        line = line.split(',')
        line[-1] = line[-1].rstrip('\n')
        csv_good_attrvals1.append(line)

csv_good_attrvals_no_pynames1 = []
for line in csv_good_attrvals1:
    line_copy = line[:]
    line_copy[0] = ""
    csv_good_attrvals_no_pynames1.append(line_copy)

csv_good_attrvals_no_mod1 = []
for line in csv_good_attrvals1:
    line_copy = line[:]
    line_copy[1] = line_copy[0]
    csv_good_attrvals_no_mod1.append(line_copy)

ftypes_bad_types = [
                    'list',
                    'tuple',
                    'Food',
                    'dict',
                    'OrderedDict'
]

fnames_bad_types = ['foo%d' % i for i in range(1, len(ftypes_bad_types) + 1)]

assert len(ftypes_bad_types) == len(fnames_bad_types)

with open(join(indir, 'extract_csv_bad_pynames.csv'), 'r') as f:
    f.readline()
    f.readline()

    csv_bad_pynames1 = []
    for line in f:
        line = line.split(',')
        line[-1] = line[-1].rstrip('\n')
        csv_bad_pynames1.append(line)


# Build this list here to make it easier to ensure properness or something
test_food_objects_fmap = [
                            ("PyName", str),
                            ("Name", str),
                            ("Protein", float),
                            ("Carbs", float),
                            ("Fat", float),
                            ("Alcohol", float),
                            ("ServingSize", float),
                            ("ServingCal", float)
                        ]
from pysrc.food_stuff.food import Food

test_food_objs_foods = [
        ["HeavyCream", "Heavy Cream", 0.0, 0.5, 5.0, 0.0, 15.0, 50.0],
        ["DarkBrownSugar", "Dark Brown Sugar", 0.0, 4.0, 0.0, 0.0, 4.0, 15.0],
        ["LargeEgg", "Large Egg", 6.29, 0.39, 5.0, 0.0, 54.0, 73.5],
        ["IForceProteanVanillaCupcakeBatter", "IForce Protean Vanilla Cupcake Batter", 20.0, 6.5, 1.0, 0.0, 34.0, 120.0],
        ["Milk1pc", "Milk 1%", 10.0, 16.0, 2.5, 0.0, 240.0, 130.0],
        ["GreekYogurt", "Greek Yogurt", 22.0, 0.0, 0.0, 0.0, 227.0, 120.0]
]

test_food_objects = OrderedDict()
for attrs in test_food_objs_foods:
    test_food_objects[attrs[0]] = Food(*attrs)
