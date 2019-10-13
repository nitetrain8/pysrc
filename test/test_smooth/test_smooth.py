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
from decimal import Decimal as D, getcontext, setcontext

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
    for dir in (temp_dir, test_input):
        try:
            makedirs(dir)
        except FileExistsError:
            pass


class Smooth(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.addTypeEqualityFunc(D, self.assertDecimalEqual)

        from decimal import Context
        self.ctx = Context(prec=12)

    def assertDecimalEqual(self, exp, result, msg=None):
        """
        @param exp:
        @type exp: D
        @param result:
        @type result:
        @return:
        @rtype:
        """
        old_ctx = getcontext()
        setcontext(self.ctx)

        # unary plus forces re-calculation of # digits
        exp = +exp
        result = +result
        not_equal = exp.compare(result)

        setcontext(old_ctx)

        if not_equal:
            raise self.failureException((msg or '') + str(exp) + ' ' + str(result))

    def do_smooth1_test(self, x, y, exp_ydata=None):
        """
        @return: None
        @rtype: None
        """

        x = tuple(map(round, x))
        y = tuple(map(D, y))

        xd, yd = smooth1(x, y)
        assertEqual = self.assertEqual

        if exp_ydata:
            for xpt, ypt, exp in zip(xd, yd, exp_ydata):
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

        self.do_smooth1_test(x, y, expected)

        x = 0, 10
        y = 0, 10
        expected = tuple(range(100))

        self.do_smooth1_test(x, y, expected)

        x = tuple(range(0, 51, 10))
        y = tuple(range(0, 51, 10))
        expected = tuple(range(51))

        self.do_smooth1_test(x, y, expected)

    def test_smooth1_2(self):
        """ floats (decimals) """
        one_hundred = D(100)

        y_data = tuple(x / one_hundred for x in range(0, 101, 20))
        x_data = tuple(range(0, len(y_data) * 2, 2))
        expected = []
        for intpart in range(0, 2):
            for decpart in range(0, 10, 1):
                expected.append(D("%d.%d" % (intpart, decpart)))

        self.do_smooth1_test(x_data, y_data, expected)

    def test_smooth1_real1(self):
        """
        """
        testfile = test_input + "\\real_smooth.csv"
        with open(testfile, 'r') as f:
            data = [x.split(',') for x in f.read().splitlines()]

        x, y = zip(*data)

        x = map(float, x)
        self.do_smooth1_test(x, y)


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
