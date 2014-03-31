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


foo = None


class TestMakeConstantsCoConsts(unittest.TestCase):

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

    def test_simple_store_global(self):
        """
        Test a function with STORE_GLOBAL opcodes
        """

        def test_globals():
            global foo
            print(foo)
            foo = 1

        expected = test_globals
        result = _make_constants(expected)

        self.assertIs(expected, result, "Function incorrectly modified")

    def test_class_method_simple(self):
        """
        Make sure the function works on class instance methods.
        """

        from io import StringIO
        dummy = StringIO()

        class TestClass():

            def testfunc(self, arg):
                foo = float(arg)
                bar = str(foo)
                baz = len(bar)
                print(baz, file=dummy)
                return baz

            def __len__(self):
                return 1

        t = TestClass()
        expected = t.testfunc
        result = _make_constants(expected)
        expected_consts = (None, 'file', float, str, len, print)

        self.check_co_consts(result, expected_consts)

        # make sure it works
        call_result = t.testfunc(12)
        exp = 4
        self.assertEqual(call_result, exp)
        self.assertEqual(str(call_result) + '\n', dummy.getvalue())


class TestMakeConstantsInOut(unittest.TestCase):

    def test_make_constants_smooth1(self):
        """
        import the unittest for smooth1. Run them once to verify passing,
        then modify the module namespace with modified function, and run again.

        This is probably not the best way to do this, but oh well.

        @return: None
        @rtype: None
        """

        from pysrc.test.test_smooth import test_smooth

        ref_smooth = test_smooth.smooth1
        new_smooth = _make_constants(ref_smooth)

        if new_smooth is ref_smooth:
            raise self.failureException("Function not modified- unexpected failure")

        test_case = test_smooth.Smooth()

        tests = (
            test_case.test_smooth1_1,
            test_case.test_smooth1_2,
            test_case.test_smooth1_real1
        )

        # Catch and re-raise each exception on failure for
        # accurate error reporting

        # first pass- assert all the other tests actually pass.
        # even though its not our fault, silently ignoring errors
        # could result in false positives.

        for test in tests:
            try:
                test()
            except self.failureException:
                raise self.failureException("Unrelated test unexpectedly failed") from None
            except:
                raise self.failureException("Unknown error from unrelated test") from None

        # Second pass- modify and see if they still pass

        for test in tests:

            test_smooth.smooth1 = new_smooth
            try:
                test()
            except self.failureException:
                # restore ref_smooth in case future tests added to run
                test_smooth.smooth1 = ref_smooth
                raise self.failureException("Mismatch result after modification in test %s" % test.__name__)


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
