"""

Created by: Nathan Starkweather
Created on: 03/29/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'

from opcode import opmap, HAVE_ARGUMENT, EXTENDED_ARG, opname

LOAD_CONST = opmap['LOAD_CONST']
STORE_GLOBAL = opmap['STORE_GLOBAL']
LOAD_GLOBAL = opmap['LOAD_GLOBAL']
GREATER_HAVE_ARG = HAVE_ARGUMENT + 1

from types import FunctionType, CodeType, MethodType

# The type constructors actually do the work, but
# providing aliases here so that it is easier to read our code.
make_function = FunctionType
make_code = CodeType
make_method = MethodType

# get pyssizet size at runtime by checking against
# the arg parsing typecode.

import ctypes as _ctypes
from weakref import ref as _wref
from ctypes import py_object as _py_object, pythonapi as _pythonapi
from _ctypes import sizeof as _csizeof, Py_DECREF as _Py_DECREF, Py_INCREF as _Py_INCREF
from struct import calcsize as _calcsize

_py_ssize_t_bytes = _calcsize('n')
if _py_ssize_t_bytes == 8:
    _Py_ssize_t = _ctypes.c_uint64
elif _py_ssize_t_bytes == 4:
    _Py_ssize_t = _ctypes.c_uint32
else:
    raise SystemError("size of _Py_ssize_t does not match known values")

# _Py_ssize_t should be the same size as ssize_t, but unsigned
if _csizeof(_ctypes.c_ssize_t) != _csizeof(_Py_ssize_t):
    raise SystemError("Ambiguous ssize_t size")

# cache to store list of weak references. We need this so that
# the weak ref object itself stays alive so that the callback can
# be called.
_hack_cache = set()


def _hack_callback(hackref):
    """

    Execute the cleanup action by the function hack weakref.
    Because the weakref callback can never be called until func's refcount
    is 0, we should NOT call Py_DECREF on the target index, or even access it
    to check, or we will segfault.

    But, we can be reasonably sure that the refcount is zero, so we can
     override that item. We don't have to worry about Py_DECREF being called
     by the C code, but if the implementation changed, we would.

    @param hackref: _FuncHackRef
    @type hackref: _FuncHackRef
    """
    # Remove the reference from the cache.
    _hack_cache.remove(hackref)

    pyob_const = _py_object(hackref.f_const)
    pyob_index = _Py_ssize_t(hackref.f_index)
    pyob_none = _py_object(None)

    rc = _Py_ssize_t.from_address(id(hackref.f_const))
    old_rc = rc.value
    rc.value = 1

    _Py_INCREF(None)
    _pythonapi.PyTuple_SetItem(pyob_const, pyob_index, pyob_none)

    rc.value = old_rc


class _FuncHackRef(_wref):

    __slots__ = 'f_const', 'f_index'

    def __new__(cls, func):
        self = super().__new__(func, _hack_callback)
        self.f_const = func.__code__.co_consts
        self.f_index = self.f_const.index(func)
        return self


def hack_tuple(ob, i, newitem):
    """
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
        raise TypeError("Can't hack non-tuple item.")

    if i >= len(ob):
        raise IndexError("Index out of range.")

    prev = ob[i]
    _Py_DECREF(prev)

    pyob_ob = _py_object(ob)
    pyob_newitem = _py_object(newitem)

    # set ref count to 1 temporarily, to avoid PyErrBadInternalCall()
    # TypeError triggered by PyTuple_SetItem if refcount > 1.
    # we could just use PyStructSequence_SetItem, but this seems more robust
    # against potential API changes, and we aren't too concerned with
    # performance here.

    rc = _Py_ssize_t.from_address(id(ob))
    old_rc = rc.value
    rc.value = 1

    _pythonapi.PyTuple_SetItem(pyob_ob, _Py_ssize_t(i), pyob_newitem)

    rc.value = old_rc


def _hack_recursive_func(new_func, old_func):
    """

    Hack the recursive function to contain a constant reference
    to itself.

    1) Use low-level capi (via hack_tuple) to mutate the co_consts
     tuple object of the function to contain a constant self-reference.
     Set the 'incref' parameter to false, as otherwise the memory would be
     leaked (as there would be no way to decrease the final reference).

    2) Set up a custom weak reference scheme that allows us to keep a
    strong reference to the co_consts tuple, with a callback called when
    the function is deleted.

    3) With function deleted, we now have a tuple with an invald reference,
    but we know which index contains that reference. Use capi again to
    quietly re-write the tuple index to contain Py_None, then delete
    the local tuple reference.

    @param new_func: new function
    @type new_func: FunctionType | MethodType
    @param old_func: old function
    @type old_func: FunctionType | MethodType
    @return: None
    @rtype: None
    """

    co_consts = new_func.__code__.co_consts
    co_index = co_consts.index(old_func)

    # Hack the tuple
    hack_tuple(co_consts, co_index, new_func, False)


def getarg(codestr, i):
    """
    @param codestr: Code string
    @type codestr: bytes | collections.Sequence[int]
    @param i: index of opcode
    @type i: int
    @return: int value of oparg
    @rtype: int
    """
    if codestr[i] < HAVE_ARGUMENT:
        raise ValueError("Opcode %s (%d) does not have argument" % (opname[codestr[i]], codestr[i]))
    oparg = codestr[i + 1] + (codestr[i + 2] << 8)
    return oparg


def _getops(codestr):
    """

    Scan codestring for all opcodes, returning list of
    2-tuples (index, opcode).

    @param codestr: code string to parse
    @type codestr: bytes | collections.Sequence[int]
    @return: 2-tuple (index, op)
    @rtype: list[(int, int)]
    """
    oplist = []; ap = oplist.append
    i = 0
    codelen = len(codestr)

    while i < codelen:
        op = codestr[i]
        ap((i, op))
        i += 1
        if op > GREATER_HAVE_ARG:
            i += 2
    return oplist


def code_maker(co, newcode, newconsts):
    return make_code(co.co_argcount, co.co_kwonlyargcount, co.co_nlocals,
                     co.co_stacksize, co.co_flags, bytes(newcode),
                     tuple(newconsts), co.co_names, co.co_varnames,
                     co.co_filename, co.co_name, co.co_firstlineno,
                     co.co_lnotab, co.co_freevars, co.co_cellvars)


def function_maker(old_func, new_code):
    return make_function(new_code, old_func.__globals__, old_func.__name__, old_func.__defaults__, old_func.__closure__)


def _make_constant_globals(f, env, verbose=False):
    """
    My implementation of make-constants function. Yay!.
    Original: http://code.activestate.com/recipes/576904/

    @param f:
    @type f: types.FunctionType
    @param env: extra stuff to include for making constants.
    @type env: dict
    @return: optimized function
    @rtype: types.FunctionType
    """

    mod = getattr(f, '__module__', 'None')
    name = f.__qualname__

    if verbose:
        print("Attempting to optimize <%s.%s>." % (mod, name))

    co = f.__code__
    newcode = list(co.co_code)
    co_names = co.co_names
    newconsts = list(co.co_consts)
    newconsts_append = newconsts.append

    env_get = env.get

    codelen = len(newcode)
    i = 0
    changed = False
    while i < codelen:
        op = newcode[i]

        if op in (EXTENDED_ARG, STORE_GLOBAL):
            # todo: store-global can be worked around with a double pass to pop offenders from env
            # todo: Extended arg: get oparg, shift << 16, i += 3, add oparg to NEXT oparg value of NEXT op
            return f

        if op == LOAD_GLOBAL:

            # Each oparg is an unsigned byte in range (0, 255).
            # If the size of co_consts is > 255, overflow would be stored
            # in newcode[i + 2] (or more, with EXTENDED_ARG).
            # Bit shift (0 << 8 == 0) and add together.

            oparg = newcode[i + 1] + (newcode[i + 2] << 8)
            name = co_names[oparg]
            value = env_get(name)

            if value is not None:

                changed = True
                for pos, v in enumerate(newconsts):
                    if v is value:
                        break
                else:
                    pos = len(newconsts)
                    newconsts_append(value)

                # Bitwise & 0xff, shift >> 8: bytes have max capacity of 255
                # use bit twiddling to store multibyte int into two bytes.

                newcode[i] = LOAD_CONST
                newcode[i + 1] = pos & 0xff
                newcode[i + 2] = pos >> 8

        i += 1
        if op >= HAVE_ARGUMENT:
            i += 2

    if not changed:
        return f

    # Make code object from type of code in case there
    # is a difference between FunctionType, MethodType, etc

    f_code = code_maker(co, newcode, newconsts)
    new_func = function_maker(f, f_code)

    if type(f) is MethodType:
        new_func = make_method(new_func, f.__self__)

    if f in new_func.__code__.co_consts:
        _hack_recursive_func(new_func, f)

    return new_func


def make_constants(env=None, blacklist=None, verbose=False, **kwargs):
    """
    public interface to _make_constant_globals, for sake of accepting whitelist
    in the form of kwargs
    @param env: pass in a dict mapping names <=> values to override. Caller
                responsible for ensuring that names map to the correct value.
    @type env: dict
    @type blacklist: dict | None
    @type verbose: bool
    @param kwargs:
    @return: make_constants function wrapper
    @rtype: types.FunctionType
    """

    import builtins

    def constants_wrapper(f):
        """
        @param f: function to wrap
        @type f: types.FunctionType
        @return: types.FunctionType
        @rtype: types.FunctionType
        """
        # Make real dict in reverse order of priority
        # most important last -> overrides earlier
        # first, default global values

        real_env = vars(builtins).copy()
        real_env.update(f.__globals__)

        # update user specified, and discard from blacklist
        # update kwargs with env has same effect as updating
        # real env with kwargs then env, but makes it easier
        # to error check vs blacklist

        if env is not None:
            kwargs.update(env)

        real_env.update(kwargs)

        if blacklist is not None:
            for key in blacklist:
                try:
                    if real_env[key] == blacklist[key]:
                        del real_env[key]
                        if verbose:
                            print("Removing %s from env for function <%s>" % (key, f.__name__))
                    else:
                        raise ValueError("Environment mapping {%r : %r} != blacklist mapping {%r : %r}"
                                         % (key, real_env[key], key, blacklist[key]))
                except KeyError:
                    pass

        return _make_constant_globals(f, real_env, verbose)

    return constants_wrapper




