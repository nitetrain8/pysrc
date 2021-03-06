"""

Created by: Nathan Starkweather
Created on: 04/09/2016
Created in: PyCharm Community Edition

Module: test_module
Functions: test_functions

"""
import pytest
from os import makedirs
import sys
# noinspection PyUnresolvedReferences
from os.path import dirname, join, exists, basename
from shutil import rmtree
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
_h = logging.StreamHandler()
_f = logging.Formatter("%(created)s %(name)s %(levelname)s (%(lineno)s): %(message)s")
_h.setFormatter(_f)
logger.addHandler(_h)
logger.propagate = False
del _h, _f

__author__ = 'Administrator'

curdir = dirname(__file__)
test_dir = dirname(curdir)
test_temp_dir = join(test_dir, "temp")
temp_dir = join(test_temp_dir, "temp_dir_path")
test_input = join(curdir, "test_input")
local_test_input = join(test_input, basename(__file__.replace(".py", "_input")))


def setup_module():
    for d in temp_dir, test_input, local_test_input:
        try:
            makedirs(d)
        except FileExistsError:
            pass
    set_up_pyfile_logger()
    sys.path.append(curdir)
    sys.path.append(local_test_input)
    print()


def set_up_pyfile_logger():
    global pyfile_logger
    pyfile_logger = logging.getLogger("pyfile_" + basename(__file__.replace(".py", "")))
    pyfile_formatter = logging.Formatter("")
    pyfile_handler = logging.FileHandler(join(test_input, local_test_input, "dbg_ut.py"), 'w')
    pyfile_logger.addHandler(pyfile_handler)
    pyfile_handler.setFormatter(pyfile_formatter)


def teardown_module():
    try:
        rmtree(temp_dir)
    except FileNotFoundError:
        pass

    for p in (curdir, local_test_input):
        try:
            sys.path.remove(p)
        except Exception:
            pass

from python import cext
from python.cext import c_types
from python.cext.c_types import *
import itertools


def show(fp):
    import subprocess
    subprocess.Popen("\"C:/program files (x86)/notepad++/notepad++.exe\" \"%s\"" % fp)


def test_CType_funcstub():
    i = c_types.CType('foo')
    mytype_del = c_types.destructor('MyType_del')
    print()
    print(mytype_del.to_string())
    mytype_printfunc = c_types.printfunc("MyType_print")
    print(mytype_printfunc.to_string())
    mytype_getattrfunc = c_types.CFunc(c_types.getattrfunc, "MyType_getattr")
    print(mytype_getattrfunc.to_string())


def test_make_stub():
    filepath = "C:/.replcache/stub.c"
    mytype = typedef(CStruct("MyType", False, False, *[
        ('foo', c_int),
        ('bar', PyObject_p),
        ('baz', CFunc.fn(PyObject_p, "baz", None, PyObject_p("self"), PyObject_p("i"), c_int))
    ]), "MyType")
    mytype2 = PyTypeObject()
    t, s = cext.empty_type_stub(mytype2)
    print(s)
    print(t)
    # show(filepath)

from python.cext import parse


# def test_tokenize_str():
#     pth = "C:\\Users\\Administrator\\Documents\\pyprojects\\python\\scripts\\toys\\empty.c"
#     with open(pth, 'r') as f:
#         src = f.read()
#     toks = parse.tokenize(src)
#     for t in toks:
#         pass

def test_parse_type_str():
    pts = parse.parse_type_str
    print(pts("const char *"))
    print(pts("long long int"))
    print(pts("struct foobar;"))
    print(pts("FILE *bar;"))



# def test_type_slots():
#     ts = cext.slot_names
#     tps = cext.all_slots
#     it = itertools.zip_longest(ts, tps, fillvalue=None)
#     for i, (n1, (t, n2)) in enumerate(it):
#         assert n1 == n2

def test_type_to_str():
    tts = type_from_str
    assert tts("const char *") == CPointer(char, 1, True)
    assert tts


if __name__ == '__main__':
    print()
    pytest.main()
