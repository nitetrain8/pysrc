"""

Created by: Nathan Starkweather
Created on: 03/29/2014
Created in: PyCharm Community Edition

Module: test_module
Functions: test_functions

"""
import unittest
from os import makedirs
from os.path import dirname, join, exists
from shutil import rmtree
from pysrc.snippets.optimize_constants import _make_constants

__author__ = 'Administrator'

curdir = dirname(__file__)
test_dir = dirname(curdir)
test_temp_dir = join(test_dir, "temp")
temp_dir = join(test_temp_dir, "temp_dir_path")
test_input = join(curdir, "test_input")


def setUpModule():

    for folder in (test_temp_dir, temp_dir, test_input):
        if not exists(folder):
            try:
                makedirs(folder)
            except OSError:
                pass


class TestMakeConstantsInner(unittest.TestCase):

    def check_co_consts(self, func, expected, msg=None):
        """
        @type func: types.FunctionType
        @type expected: tuple
        @type msg: None | str
        @return:
        @rtype:
        """

        result = func.__code__.co_consts

        if type(expected) is not type(result):
            expected = type(result)(expected)

        self.assertEqual(result, expected, msg)

    def test_simple_builtins1(self):
        """
        @return: None
        @rtype: None
        """

        def testfunc1(dummy):
            print(len(dummy))

        expected = (None, print, len)
        result_func = _make_constants(testfunc1)

        self.assertIsNotNone(result_func, "Forgot to return function!")
        self.assertIsNot(result_func, testfunc1, "Function not modified")
        self.check_co_consts(result_func, expected, "testfunc1")

    def test_simple_buitins2(self):

        def testfunc2(dummy):
            dummy_len = len(dummy)
            print(dummy_len)

        expected = (None, len, print)
        result_func = _make_constants(testfunc2)

        self.assertIsNotNone(result_func, "Forgot to return function!")
        self.assertIsNot(result_func, testfunc2, "Function not modified")
        self.check_co_consts(result_func, expected, 'testfunc2')


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
