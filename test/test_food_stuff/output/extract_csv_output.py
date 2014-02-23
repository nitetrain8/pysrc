"""

Created by: Nathan Starkweather
Created on: 02/22/2014
Created in: PyCharm Community Edition

Hold some python objects which should be replicated by the test functions.
Sometimes it is easier to build the test objects at runtime,
sometimes it is easier to write them in here.

Time will tell which is better.
"""
from os.path import dirname, join, normpath

outputdir = dirname(__file__)
testdir = dirname(outputdir)
indir = join(testdir, "input")

indir = normpath(indir)
testdir = normpath(testdir)
outputdir = normpath(outputdir)

with open(join(indir, "extract_csv_good1.csv"), 'r') as f:
    csv_good1_fnames = f.readline().rstrip('\n').split(',')
    csv_good1_ftypes = f.readline().rstrip('\n').split(',')

    csv_good1_attrvals = []
    for line in f:
        line = line.split(',')
        line[-1] = line[-1].rstrip('\n')
        csv_good1_attrvals.append(line)

csv_good1_attrvals_no_pynames = []
for line in csv_good1_attrvals:
    line_copy = line[:]
    line_copy[1] = ""
    csv_good1_attrvals_no_pynames.append(line_copy)

csv_good1_attrvals_no_mod = []
for line in csv_good1_attrvals:
    line_copy = line[:]
    line_copy[1] = line_copy[0]
    csv_good1_attrvals_no_mod.append(line_copy)

ftypes_bad_types = [
                    'list',
                    'tuple',
                    'Food',
                    'dict',
                    'OrderedDict'
]

fnames_bad_types = ['foo%d' % i for i in range(1, len(ftypes_bad_types) + 1)]

assert len(ftypes_bad_types) == len(fnames_bad_types)
