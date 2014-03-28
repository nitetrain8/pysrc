"""

Created by: Nathan Starkweather
Created on: 03/27/2014
Created in: PyCharm Community Edition

Module: test_module
Functions: test_functions

"""
import unittest
from os import makedirs
from os.path import dirname, join
from shutil import rmtree
from pysrc.snippets.smooth import smooth1
from decimal import Decimal as D

__author__ = 'Administrator'

curdir = dirname(__file__)
test_dir = dirname(curdir)
test_temp_dir = join(test_dir, "temp")
temp_dir = join(test_temp_dir, "temp_dir_path")
test_input = join(curdir, "test_input")


def setUpModule():

    """
    @return: None
    @rtype: None
    """
    try:
        makedirs(temp_dir)
    except FileExistsError:
        pass


class Smooth(unittest.TestCase):

    def do_smooth_test(self, x, y, expected):
        """
        @return: None
        @rtype: None
        """

        x = tuple(map(round, x))
        y = tuple(map(D, y))

        xd, yd = smooth1(x, y)
        assertEqual = self.assertEqual

        for xpt, ypt, exp in zip(xd, yd, expected):
            assertEqual(ypt, exp)

        for xpt, ypt in zip(x, y):
            assertEqual(yd[xpt], ypt)

        assertEqual(yd[0], y[0])
        assertEqual(yd[-1], y[-1])

        x_start = x[0]
        y_start = y[0]
        for ypt in yd[:x_start + 1]:
            assertEqual(ypt, y_start)

        exp_size = x[-1] + 1
        assertEqual(len(yd), exp_size)
        assertEqual(len(xd), exp_size)

    def test_smooth1_1(self):
        x = (1, 100)
        y = (1, 100)
        expected = list(range(100))
        expected[0] = 1

        self.do_smooth_test(x, y, expected)

        x = 0, 10
        y = 0, 10
        expected = tuple(range(100))

        self.do_smooth_test(x, y, expected)

        x = tuple(range(0, 51, 10))
        y = tuple(range(0, 51, 10))
        expected = tuple(range(51))

        self.do_smooth_test(x, y, expected)




def tearDownModule():
    """
    @return: None
    @rtype: None
    """
    try:
        rmtree(temp_dir)
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    unittest.main()
