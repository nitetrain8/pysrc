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
import builtins

from pysrc.optimize._ctypes_hax import _tuple_set_item, getrefptr
from pysrc.optimize.optimize_constants import _make_constant_globals, make_constants


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

    @classmethod
    def setUpClass(cls):
        cls.test_env = vars(builtins).copy()

    def check_co_consts(self, func, expected, msg=None):
        """
        @type func: types.FunctionType
        @type expected: tuple | list
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
        result_func = _make_constant_globals(testfunc1, self.test_env)

        self.assertIsNotNone(result_func, "Forgot to return function!")
        self.assertIsNot(result_func, testfunc1, "Function not modified")
        self.check_co_consts(result_func, expected, "testfunc1")

    def test_simple_buitins2(self):

        def testfunc2(dummy):
            dummy_len = len(dummy)
            print(dummy_len)

        expected = (None, len, print)
        result_func = _make_constant_globals(testfunc2, self.test_env)

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
        result = _make_constant_globals(expected, self.test_env)

        self.assertIs(expected, result, "Function incorrectly modified")

    def test_class_method_simple(self):
        """
        Make sure the function works on class instance methods.
        """

        from io import StringIO
        dummy = StringIO()

        class TestClass():

            # noinspection PyMethodMayBeStatic
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
        result = _make_constant_globals(expected, self.test_env)
        expected_consts = (None, 'file', float, str, len, print)

        self.check_co_consts(result, expected_consts)

        # make sure it works
        call_result = t.testfunc(12)
        exp = 4
        self.assertEqual(call_result, exp)
        self.assertEqual(str(call_result) + '\n', dummy.getvalue())


class TestMakeConstantsInOut(TestMakeConstantsCoConsts):

    def assertDecimalEqual(self, result, expected, msg=None):
        """
        @param result:
        @type result:
        @param expected:
        @type expected:
        @param msg:
        @type msg:
        @return:
        @rtype:
        """

        from decimal import localcontext

        with localcontext() as ctx:
            ctx.prec = 3  # not testing decimal precision atm
            res = +result
            exp = +expected

            cmp = res == exp

        if not cmp:
            if msg is None:
                msg = ''

            msg += "Decimals do not match: %.3f != %.3f" % (res, exp)
            raise self.failureException(msg)

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
        new_smooth = _make_constant_globals(ref_smooth, self.test_env)

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

    def test_make_constants_est_env(self):
        """
        Test runtime function created during an ipython session.
        """

        # Defining function here results in LOAD_DEREF instead of
        # LOAD_GLOBAL, so exec the source code in a custom global namespace.

        from scripts.run.temp_sim import TempSim, D

        funcdef = """def est_env(pv):
    env = pv * c / (h * hd)
    return env
"""

        ns = {
            'hd' : D('4.5'),
            'c' : TempSim.DEFAULT_COOL_CONSTANT,
            'h' : TempSim.DEFAULT_HEAT_CONSTANT,
        }

        exec(funcdef, ns, ns)
        est_env = ns['est_env']

        exp_consts = [None]
        self.check_co_consts(est_env, exp_consts)

        Decimal = D

        x_values = tuple(range(15))
        y_values = [
            Decimal('-0.000000'),
            Decimal('-0.09120879781676413255360623782'),
            Decimal('-0.1824175956335282651072124756'),
            Decimal('-0.2736263934502923976608187135'),
            Decimal('-0.3648351912670565302144249513'),
            Decimal('-0.4560439890838206627680311891'),
            Decimal('-0.5472527869005847953216374269'),
            Decimal('-0.6384615847173489278752436647'),
            Decimal('-0.7296703825341130604288499025'),
            Decimal('-0.8208791803508771929824561404'),
            Decimal('-0.9120879781676413255360623782'),
            Decimal('-1.003296775984405458089668616'),
            Decimal('-1.094505573801169590643274854'),
            Decimal('-1.185714371617933723196881092'),
            Decimal('-1.276923169434697855750487329')
        ]

        result1 = [est_env(x) for x in x_values]

        assertDecimalEqual = self.assertDecimalEqual

        for res, exp in zip(result1, y_values):
            assertDecimalEqual(res, exp, "Test failed initial pass")

        # modify the function. While we're here, pass in a bad namespace
        # to test blacklist

        bad_blacklist = {'hd' : 'bobcat'}

        bad_wrapper = make_constants(ns, bad_blacklist)
        self.assertRaises(ValueError, bad_wrapper, est_env)

        modified_env = make_constants(ns, None, True)(est_env)
        result2 = [modified_env(x) for x in x_values]

        for res, exp in zip(result2, y_values):
            assertDecimalEqual(res, exp, "Modified function produced bad result")

        exp_consts.extend((ns['c'], ns['h'], ns['hd']))
        self.check_co_consts(modified_env, exp_consts)


class TestHax(TestMakeConstantsCoConsts):

    def test_hack_tuple_recursive(self):

        mytuple = (1, 2, 3)
        self.assertRaises(TypeError, _tuple_set_item, list(mytuple), 1, mytuple)

        _tuple_set_item(mytuple, 1, mytuple)
        self.assertIs(mytuple[1], mytuple)

    def test_hack_tuple_memleak(self):
        # Make sure hack tuple doesn't leave memory leaks

        import gc
        from pysrc.optimize._ctypes_hax import _Py_ssize_t

        # Cast unsigned -1 to python int
        rfc_expected = _Py_ssize_t(-1).value

        # XXX DO NOT CHANGE THIS!
        # If built using a tuple literal, tuple will be ref'd as a
        # code/frame constant and be off by 1 for the test.
        # reference mytuple in a closure function to be sure
        # that all refs are gone.
        # also, DO NOT NOT MAKE ANY PYOBJECTS after running this!
        # if a pyobject is made, it may be made at the address
        # of mytuple, and throw off the resulting refcount.

        def run_test():
            mytuple = tuple([1, 2, 3])

            rfc = getrefptr(mytuple)

            self.assertTrue(gc.is_tracked(mytuple))
            self.assertEqual(rfc.value, 1)
            b = mytuple
            self.assertEqual(rfc.value, 2)
            del b
            self.assertEqual(rfc.value, 1)

            _tuple_set_item(mytuple, 1, mytuple)
            self.assertEqual(rfc.value, 1)

            mytuple = None
            del mytuple
            return rfc
        rfc = run_test()

        # Because tuples 'cannot' have references to themselves,
        # the tuple deallocator reduces refcount to -1 due to
        # nested reference. This will cause memory leaks, but we test for
        # its presense to keep an eye on the behavior of the code.
        # XXX Not sure if the above is actually true

        self.assertEqual(rfc.value, rfc_expected)
        gc.collect()  # if interpreter segfaults, the test failed :-)

    def test_dirwalk(self):

        # Optimizing a recursive function to have a reference to itself,
        # when a global name is not defined but added to the function through make_constants
        # causes a NameError to occur, because the 'constant' self-reference actually
        # refers to the old function.

        from pysrc.test.test_optimize_constants.test_input.fix_dirwalk import dirwalk
        from os import listdir

        dirwalk = make_constants(dirwalk=dirwalk, listdir=listdir, OSError=OSError, join='\\'.join)(dirwalk)
        dirwalk = make_constants(dirwalk=dirwalk)(dirwalk)

        dirwalk(curdir)
        rc = getrefptr(dirwalk)

        self.assertEqual(rc.value, 1)

        import gc

        del dirwalk
        gc.collect()

        self.assertEqual(rc.value, 0)


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
