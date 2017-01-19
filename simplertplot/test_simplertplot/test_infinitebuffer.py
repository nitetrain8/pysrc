"""

Created by: Nathan Starkweather
Created on: 04/16/2016
Created in: PyCharm Community Edition

Module: test_module
Functions: test_functions

"""
import itertools
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

import numpy as np
from python.simplertplot.queues import InfiniteBuffer
from itertools import zip_longest


def test_infbuffer_basic():
    l = list(range(5))
    n = np.arange(5)
    g = range(5)
    exp = 0, 1, 2, 3, 4
    error = object()
    for it in (l, n, g):
        b = InfiniteBuffer(it)
        rv = b.get()
        cmp_b(exp, rv)
        assert len(b) == 5
        assert len(b._queue) == 1000
        assert not sys.getsizeof(b._queue) % 4096


def get(b):
    return b.get().tolist()

def test_infbuffer_append():
    b = InfiniteBuffer()
    b.append(1)
    assert get(b) == [1]
    b.append(2)
    assert get(b) == [1, 2]


def test_infbuffer_extend():
    b = InfiniteBuffer()
    l = list(range(100))
    b.extend(l)
    assert get(b) == l
    l2 = list(range(100, 200))
    b.extend(l2)
    assert get(b) == l + l2


def test_infbuffer_resize():
    b = InfiniteBuffer()
    it = itertools.count(1)
    l = []
    n = 0

    def addn():
        nonlocal n, it, l, b
        n = next(it)
        l.append(n)
        b.append(n)

    while len(b) != b._sz:
        addn()
        check_sz(b, 1)

    addn()
    check_sz(b, 2)


def check_sz(b, pgs=1):
    __tracebackhide__ = True
    assert sys.getsizeof(b._queue) == 4096 * pgs


def cmp_b(l, b):
    error = object()
    for e, r in zip_longest(l, b, fillvalue=error):
        assert error not in (e, r)
        assert e == r


def test_infbuffer_extend_resize():
    b = InfiniteBuffer()
    it = itertools.count(1)
    l = []
    n = 0

    def extd(i):
        nonlocal b, it, l, n
        tmp = [next(it) for _ in range(i)]
        b.extend(tmp)
        l.extend(tmp)

    extd(998)
    check_sz(b, 1)
    extd(1)
    check_sz(b, 1)
    extd(1)
    check_sz(b, 1)
    extd(1)
    check_sz(b, 2)
    extd(1023)
    check_sz(b, 2)
    extd(10)
    check_sz(b, 3)






if __name__ == '__main__':
    pytest.main()
