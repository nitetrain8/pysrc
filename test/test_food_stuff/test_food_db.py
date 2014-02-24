__author__ = 'Administrator'

# Stuff to test
from pysrc.food_stuff.food_db import db_write_header, db_init_foods, get_foods_csv, load_raw_csv, assert_pynames, \
    name_to_pyname_repl, name_to_pyname, __save_bkup_cache, build_field_map, build_food_objects

from pysrc.food_stuff.food import Food

# reference to module for various reasons including __dict__ access
from pysrc.food_stuff import food_db


# Test input/output stuff
from pysrc.test.test_food_stuff.output.extract_csv_output import csv_good_fnames1, csv_good_ftypes1, csv_good_attrvals1, \
    csv_good_attrvals_no_mod1, csv_good_attrvals_no_pynames1, ftypes_bad_types, fnames_bad_types, csv_bad_pynames1, \
    test_food_objects_fmap, test_food_objects, \
    test_food_objs_foods


# Misc imports
import unittest
from os import remove as os_remove, mkdir, stat
from shutil import rmtree
from io import StringIO

import atexit
atexit.unregister(__save_bkup_cache)

from os.path import dirname, normpath, exists

curdir = dirname(__file__)
input_dir = curdir + "\\input"
output_dir = curdir + "\\output"
temp_dir = dirname(curdir) + "\\temp"

# Normalize paths
curdir = normpath(curdir)
input_dir = normpath(input_dir)
output_dir = normpath(output_dir)
temp_dir = normpath(temp_dir)


def reset_temp_dir(temp_dir=temp_dir):
    """
    Remove and remake the temp dir by calling rmtree
    and mkdir
    @param temp_dir: dir to remove. default to temp_dir. included instead of calling
                    global just in case I want to call it on something else.
    @return:
    @rtype:
    """
    try:
        rmtree(temp_dir)
    except FileNotFoundError:
        pass
    mkdir(temp_dir)


class TestFoodInit(unittest.TestCase):
    """
    Test all of the functions that end up in db_init_foods

    Note: all file paths normalized by normpath for
    comparison. Normpath is called a bit excessively, but
    better safe than sorry.
    """

    def setUp(self):

        self.db_header_output = output_dir + "\\test_db_header_output.csv"

        with open(self.db_header_output, 'r') as f:
            self.db_init_expected = f.read()

        # change mock directory. Need to access module dict rather than assigning attribute.
        food_db.__dict__['__curdir'] = temp_dir

        # Avoid side effects during testing

        self.mock_data_path = normpath(temp_dir + "\\data")

    def test_db_write_header(self):
        """
        Ensure that the fields written to the db header are written correctly.
        Will need to update this test fields

        @return: None
        @rtype: None
        """
        testfunc = db_write_header
        buf = StringIO()

        for test_fields, expected in self.generate_init_results():
            testfunc(buf, test_fields)
            result = buf.getvalue()
            self.assertEqual(result, expected)
            buf.truncate()

    def generate_init_results(self):
        """
        Yield (input, output) pairs for testing
        db_write_header function.


        @return: tuple of (base fields, expected output) for db_write_header func
        @rtype: __generator[(list[(str, type)], str)]
        """

        test_fields1 = [
                        ("PyName", str),
                        ("Name", str),
                        ("Protein", float),
                        ("Carbs", float),
                        ("Alcohol", float),
                        ("ServingSize", float),
                        ("ServingCal", float)
                        ]

        expected_result1 = self.db_init_expected
        yield test_fields1, expected_result1

    def test_db_init_foods_result(self):
        """
        Test db_init_foods given valid input

        @return: None
        @rtype: None
        """
        testfunc = db_init_foods
        tempfile = normpath(temp_dir + "\\db_init_foods_tmp.csv")

        # Test writing
        for test_fields, expected in self.generate_init_results():
            result_fname = testfunc(tempfile, test_fields)
            self.assertEqual(tempfile, result_fname)

            with open(result_fname, 'r') as f:
                result = f.read()

            self.assertEqual(result, expected)
            os_remove(tempfile)

    def test_db_init_foods_bad_filename(self):
        """
        Ensure that db_init_foods raises (or doesn't)
        depending on if filepath passed is valid or not.

        @return:
        @rtype:
        """

        testfunc = get_foods_csv
        self.setup_mock_data_path()

        # If exception thrown, test should fail
        try:
            result = normpath(testfunc())
        except FileNotFoundError:
            self.fail()
        else:
            expected = normpath(temp_dir + "\\data\\foods.csv")
            self.assertEqual(expected, result)
        finally:
            self.teardown_mock_data_path()

    def test_get_foods_csv(self):
        """
        @return: None
        @rtype: None
        """

        testfunc = get_foods_csv

        # Raise with no args and no directory made
        self.teardown_mock_data_path()
        self.assertRaises(testfunc)

        self.setup_mock_data_path()
        try:
            result = normpath(testfunc())
        except FileNotFoundError:
            self.fail()
        else:
            expected = normpath(temp_dir + "\\data\\foods.csv")
            self.assertEqual(expected, result)
        finally:
            self.teardown_mock_data_path()

        testpath = temp_dir + "\\temp\\temp\\temp\\foods.csv"
        base_test_dir = temp_dir + "\\temp"

        # test_paths is a list of filepaths to csv files
        # which correspond to the output from each iteration
        # of generate_init_results()

        test_paths = [
                    testpath
                    ]

        expected_results = self.generate_init_results()

        for test_path, (_, expected) in zip(test_paths, expected_results):

            reset_temp_dir(base_test_dir)

            # Call func first time -> file doesn't exist
            assert not exists(test_path)
            result = testfunc(test_path)
            result = normpath(result)
            self.assertEqual(test_path, result)
            with open(result, 'r') as f:
                result_txt = f.read()
            self.assertEqual(result_txt, expected)

            # Call func second time -> file does exist
            assert exists(test_path)
            result = testfunc(test_path)
            result = normpath(result)
            self.assertEqual(test_path, result)
            with open(result, 'r') as f:
                result_txt = f.read()
            self.assertEqual(result_txt, expected)

        # file exists at this point. Ensure calling make_new creates a new file.

        # noinspection PyUnboundLocalVariable
        assert exists(test_path)

        current_time = stat(test_path).st_mtime_ns

        from time import sleep
        sleep(0.0001)

        testfunc(test_path, make_new=True)
        new_time = stat(test_path).st_mtime_ns

        self.assertNotEqual(current_time, new_time)

    def setup_mock_data_path(self):
        """
        Set up the mock curdir + \\data directory
        as used by the db_init_foods function chain
        @return: None
        @rtype: None
        """
        try:
            mkdir(self.mock_data_path)
        except FileExistsError:
            pass

    def teardown_mock_data_path(self):
        """
        Tear down the mock curdir + \\data directory
        as used by the db_init_foods function chain
        @return: None
        @rtype: None
        """
        try:
            rmtree(self.mock_data_path)
        except FileNotFoundError:
            pass


class MockMatch():
    """ Mock interface to re.match object.
    """
    def __init__(self, rv):
        self.rv = rv

    def group(self, _):
        return self.rv


class TestCSVExtract(unittest.TestCase):

    def setUp(self):
        """
        @return:
        @rtype:
        """
        self.good_input1 = input_dir + "\\extract_csv_good1.csv"

        self.good1_fnames = csv_good_fnames1
        self.good1_ftypes = csv_good_ftypes1
        self.good1_attrvals = csv_good_attrvals1

        self.good1_attrvals_no_mod = csv_good_attrvals_no_mod1
        self.good1_attrvals_no_pynames = csv_good_attrvals_no_pynames1

        self.attrvals_bad_pynames1 = csv_bad_pynames1

        self.name_to_pyname_csv = input_dir + "\\name_to_pyname.csv"

        # Max split at 2: Name column, Pyname column, Regex column
        # max split in case commas in regex column
        with open(self.name_to_pyname_csv, 'r') as f:
            _ = f.readline()
            self.name_to_pyname_list = [line.split(',', 2) for line in f.read().splitlines()]

    def test_load_raw_csv(self):
        """
        Test raw csv
        @return:
        @rtype:
        """
        testfunc = load_raw_csv

        result_vals, result_fnames, result_ftypes = testfunc(self.good_input1)

        self.assertEqual(self.good1_fnames, result_fnames)
        self.assertEqual(self.good1_ftypes, result_ftypes)
        for expected_vals, result_vals in zip(self.good1_attrvals, result_vals):
            self.assertEqual(expected_vals, result_vals)

    def test_assert_pynames_no_mod(self):
        """
        Test the assert pynames function.
        @return:
        @rtype:
        """

        testfunc = assert_pynames
        test_no_mod = self.good1_attrvals_no_mod

        # Assert no modification
        foods_list = [food[:] for food in test_no_mod]

        testfunc(foods_list)

        for result_line, expected_line in zip(foods_list, test_no_mod):
            self.assertEqual(result_line, expected_line)

        # Assert well-formed, rectangular set of data.
        # iterate old fashion way to avoid modifying list during iteration
        # -1 because on the last iteration, all lists will be the same length
        # again.
        for i in range(len(foods_list) - 1):
            foods_list[i].pop()
            self.assertRaises(AssertionError, testfunc, foods_list)

    def test_assert_pynames_full_list(self):
        """
        @return:
        @rtype:
        """

        testfunc = assert_pynames
        in_attrs = [line[:] for line in self.good1_attrvals_no_pynames]

        expected = self.good1_attrvals

        testfunc(in_attrs)
        for expected_line, result_line in zip(expected, in_attrs):
            self.assertEqual(expected_line, result_line)

    def test_assert_pynames_override_bad(self):
        """
        Ensure that assert_pynames overrides bad pynames.
        @return:
        @rtype:
        """

        testfunc = assert_pynames
        expected = self.good1_attrvals

        result = [line[:] for line in self.attrvals_bad_pynames1]

        testfunc(result)

        for expected_line, result_line in zip(expected, result):
            self.assertEqual(expected_line, result_line)

    # noinspection PyTypeChecker
    def test_name_to_pyname_repl(self):
        """
        Short and easy. Only two possible return values.

        @return:
        @rtype:
        """

        testfunc = name_to_pyname_repl

        mock = MockMatch('%')
        result = testfunc(mock)
        self.assertEqual('pc', result)

        # generate ascii values, skip the ascii value for '%'
        for i in range(32, 37):
            mock.rv = chr(i)
            result = testfunc(mock)
            self.assertEqual('', result)

        mock.rv = "%%"
        result = testfunc(mock)
        self.assertEqual('pc', result)

    def test_name_to_pyname(self):
        """
        Test name_to_pyname by calling a list of names, pynames, (optional) regex.
        If regex entry is empty, call the function without the argument, to test
        the default regex used by the function.

        @return:
        @rtype:
        """
        testfunc = name_to_pyname

        name_list = self.name_to_pyname_list
        for name, expected_name, regex in name_list:
            if not regex:
                result = testfunc(name)
            else:
                result = testfunc(name, regex)
            self.assertEqual(expected_name, result)


class TestTypeMapping(unittest.TestCase):

    def setUp(self):
        """
        @return:
        @rtype:
        """

        self.ftypes_good1 = csv_good_ftypes1
        self.fnames_good1 = csv_good_fnames1

        self.ftypes_bad1 = ftypes_bad_types
        self.fnames_bad1 = fnames_bad_types

    def test_build_field_map(self):
        """
         Test build_field_map

         This function is actually kind of hard to test because it
         is so simple.
        @return:
        @rtype:
        """

        testfunc = build_field_map

        ftypes = self.ftypes_good1
        fnames = self.fnames_good1
        result = testfunc(fnames, ftypes)

        for (result_typename, result_type), ftype, fname in zip(result, ftypes, fnames):
            self.assertEqual(fname, result_typename)
            self.assertEqual(result_type.__name__, ftype)


class TestBuildFoods(unittest.TestCase):

    def setUp(self):
        """
        @return:
        @rtype:
        """

        self.foods_list = test_food_objs_foods
        self.objs_fmap = test_food_objects_fmap
        self.food_objs = test_food_objects

    def test_build_food_objects(self):
        """
        @return:
        @rtype:
        """
        testfunc = build_food_objects

        # Assume that build_field_map works correctly
        expected = self.food_objs
        result = testfunc(self.objs_fmap, self.foods_list)

        for exp_key, result_key in zip(expected, result):
            self.assertEqual(exp_key, result_key)
            exp_food, result_food = expected[exp_key], result[result_key]

            # Test fails using assertEqual directly since food object
            # does not currently (2/23/2014) support rich comparison.
            for attr in vars(exp_food):
                exp_attr = getattr(exp_food, attr)
                result_attr = getattr(result_food, attr)
                self.assertEqual(exp_attr, result_attr)


if __name__ == '__main__':
    unittest.main(verbosity=9)
