"""

Created by: Nathan Starkweather
Created on: 04/10/2014
Created in: PyCharm Community Edition


"""
from _weakref import ref as _wref
from ctypes import py_object as _py_object, pythonapi as _pythonapi, \
    c_ssize_t as _ssize_t, c_ushort as _ushort, \
    c_uint as _uint, c_ulong as _ulong, c_ulonglong as _ulonglong
from _ctypes import sizeof as _csizeof, Py_INCREF as _Py_INCREF

__author__ = 'Nathan Starkweather'

# Note: PyTuple_SetItem calls XDECREF on the previous item
# PyStructSequence_SetItem DOES NOT (which is what is used here)
# This is important, because it means we can call PyStructSequence_SetItem
# on invalid (deleted) objects.

_PyHack_SetItem = _pythonapi.PyStructSequence_SetItem

#: @type: list[_ctypes.PyCSimpleType]
_size_map = [None for _ in range(9)]
_type = None
for _type in (_ushort, _uint, _ulong, _ulonglong):
    _size_map[_csizeof(_type)] = _type
del _type

# Py_ssize_t is the unsigned compliment to the signed ssize_t
_py_ssize_t_bytes = _csizeof(_ssize_t)

#: @type: _ctypes.PyCSimpleType
_Py_ssize_t = _size_map[_py_ssize_t_bytes]


# =====================================================
# Tuple/Function Hacking Protocol
# =====================================================


# cache to store list of weak references. We need this so that
# the weak ref object itself stays alive so that the callback can
# be called. In Python 3.4 we can just use weakref.finalize instead.

_hack_cache = set()


def _func_hack_callback(hackref):
    """

    Execute the cleanup action by the function hack weakref.
    Because the weakref callback can never be called until func's refcount
    is 0, we should NOT call Py_DECREF on the target index, or even access it
    to check, or we will segfault.

    But, we can be reasonably sure that the refcount is zero, so we can
     override that item. We don't have to worry about Py_DECREF being called
     on an undefined object because of our choice of function, but if the C API
     implementation changed, we would.

    @param hackref: _FuncHackRef
    @type hackref: _FuncHackRef
    """
    # refcount of new_func should be 3:
    # ref in calling function (1), ref as parameter here (2),
    # and reference held by the frame object (3)
    # func_rc = _Py_ssize_t.from_address(hackref.f_addr)

    # Remove the reference from the cache!
    _hack_cache.remove(hackref)
    _Py_INCREF(None)
    _tuple_set_item(hackref.f_const, hackref.f_index, None)


class _FuncHackRef(_wref):

    __slots__ = 'f_const', 'f_index', 'ref_cb', 'f_addr'

    def __new__(cls, func, f_consts, f_index):

        self = super().__new__(cls, func, _func_hack_callback)
        self.ref_cb = _func_hack_callback
        self.f_addr = id(func)
        self.f_const = f_consts
        self.f_index = f_index
        return self

    # noinspection PyUnusedLocal
    def __init__(self, func, f_consts, f_index):
        super().__init__(func, self.ref_cb)
        _hack_cache.add(self)


def _tuple_hack_callback(hackref):
    """
    @param hackref: _TupleHackRef
    @type hackref: _TupleHackRef
    @return: None
    @rtype: None
    """
    _hack_cache.remove(hackref)
    v = hackref.replacement
    _Py_INCREF(v)
    _tuple_set_item(hackref.tpl, hackref.t_index, v)


class _TupleHackRef(_wref):

    """ Generic weakref for hacking a tuple.

    "container" is an object whose deletion indicates that
    item at "index" in "tpl" needs to be replaced with
    "replacement". This is needed because tuple objects are not
    weakrefable, so we need some other weakreferenceable object
    to indicate that its time to fix the tuple.

    """

    __slots__ = 'sentinel', 'tpl', 't_index', 'sent_id', 'cb', 'replacement'

    def __new__(cls, sentinel, tpl, index, replacement=None):

        self = super().__new__(cls, sentinel, _tuple_hack_callback)
        self.cb = _tuple_hack_callback
        self.tpl = tpl
        self.t_index = index
        self.sent_id = id(sentinel)
        self.replacement = replacement

    # noinspection PyUnusedLocal
    def __init__(self, sentinel, tpl, index, replacement=None):
        super().__init__(self, sentinel, self.cb)


def _tuple_set_item(ob, i, newitem):
    """

    Python interface to CPython API function PyStructSequence_SetItem.
    Handles conversion of arguments properly from python-space objects
    to ctypes equivalents.

    LIKE THE C API FUNCTION, DOES NOT INCREASE REF OF NEW ITEM.
    UNLIKE C API FUNCTION, DOES NOT DECREASE REF OF OLD ITEM.

    @param ob: tuple
    @type ob: tuple
    @param i: index
    @type i: int
    @param newitem: new item
    @type newitem: T
    @return:
    @rtype:
    """
    # Set the ith item of sequence item ob to newitem
    # using python capi exposed by _ctypes. While most python capi
    # performs runtime type checking, we can use PyStructSequence_SetItem
    # to arbitrarily set the item. Perform some checking here to make sure
    # we don't screw everything up.

    if type(ob) is not tuple:
        raise TypeError("Refusing to hack non-tuple item.")

    if i >= len(ob):
        raise IndexError("Index out of range.")

    pyob_ob = _py_object(ob)
    pyob_newitem = _py_object(newitem)
    pyob_i = _Py_ssize_t(i)

    _PyHack_SetItem(pyob_ob, pyob_i, pyob_newitem)


def _add_function_hack(f, f_tuple, f_index):
    """
    Modify the tuple object associated with function.

    @param f: function
    @type f: types.FunctionType
    @param f_tuple: tuple (ex co_consts, etc)
    @type f_tuple: tuple
    @param f_index: index of tuple containing overridden value
    @type f_index: int
    @return: None
    @rtype: None
    """
    hackref = _FuncHackRef(f, f_tuple, f_index)
    _hack_cache.add(hackref)


# =====================================================
# Misc Utility funcs
# =====================================================

def getref(ob):
    return _Py_ssize_t.from_address(id(ob)).value


def getrefptr(ob):
    return _Py_ssize_t.from_address(id(ob))
