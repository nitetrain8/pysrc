"""

Created by: Nathan Starkweather
Created on: 04/07/2014
Created in: PyCharm Community Edition

Module: test_module
Functions: test_functions

"""
import unittest
from os import makedirs
from os.path import dirname, join, exists
from shutil import rmtree
from weakref import ref
import pysrc.snippets.optimize_constants as optimize_constants

__author__ = 'Administrator'

curdir = dirname(__file__)
test_dir = dirname(curdir)
test_temp_dir = join(test_dir, "temp")
temp_dir = join(test_temp_dir, "temp_dir_path")
test_input = join(curdir, "test_input")


from ctypes import c_uint64, c_uint32, c_ssize_t, sizeof
if sizeof(c_ssize_t) == sizeof(c_uint64):
    Py_ssize_t = c_uint64
elif sizeof(c_ssize_t) == sizeof(c_uint32):
    Py_ssize_t = c_uint32
else:
    raise SystemError("Bad ssizet")


def getref(ob):
    return Py_ssize_t.from_address(id(ob)).value


def setUpModule():
    for folder in (test_temp_dir, temp_dir, test_input):
        if not exists(folder):
            try:
                makedirs(folder)
            except OSError:
                pass


# noinspection PyProtectedMember
class TestHackCallback(unittest.TestCase):
    def test_hack_callback(self):
        """
        @return: None
        @rtype: None
        """

        class DummyRef():
            def __init__(self, tpl, i):
                self.f_addr = id(tpl)
                self.f_const = tpl
                self.f_index = i

        # construct tuples using tuple constructor, so that no local
        # reference to the tuple as a constant exists.
        # also be carefull with specific values, such that the tuple is actually
        # unique. tuple([1, 2, 3]) tends to fail for some reason.
        a = 'hello'
        b = 2
        c = 'world'

        tpl1 = tuple([a, b, c])
        rc = getref(tpl1)
        # tpl2 = tpl1  # extra refcount

        none_refs = getref(None)

        bref = getref(b)

        dummy_ref = DummyRef(tpl1, 1)

        cache = optimize_constants._hack_cache
        cache.add(dummy_ref)
        self.assertIn(dummy_ref, optimize_constants._hack_cache)

        optimize_constants._hack_callback(dummy_ref)

        self.assertIs(tpl1[1], None)
        self.assertEqual(none_refs + 1, getref(None))
        self.assertEqual(getref(tpl1) - 1, rc)  # -1, frame object stores an extra reference
        self.assertEqual(getref(b), bref)

        self.assertNotIn(dummy_ref, optimize_constants._hack_cache)

    def test_tuple_set_item(self):
        a = 'foo '.strip()
        test_tuple = (1, a, 3)
        new_value = 'hello world'

        a_refs = getref(a)
        new_value_refs = getref(new_value)
        optimize_constants._tuple_set_item(test_tuple, 1, new_value)

        self.assertEqual(a_refs, getref(a))
        self.assertEqual(new_value_refs, getref(new_value))




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
