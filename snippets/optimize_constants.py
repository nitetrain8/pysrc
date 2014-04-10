"""

Created by: Nathan Starkweather
Created on: 03/29/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'

__all__ = [
            'make_constants',
            'bind_all',
            'ConstantOptimizingMeta'
            ]

from opcode import opmap, HAVE_ARGUMENT, EXTENDED_ARG, opname

LOAD_CONST = opmap['LOAD_CONST']
STORE_GLOBAL = opmap['STORE_GLOBAL']
LOAD_GLOBAL = opmap['LOAD_GLOBAL']
GREATER_HAVE_ARG = HAVE_ARGUMENT + 1

from types import FunctionType, CodeType, MethodType

# The type constructors actually do the work, but
# providing aliases here so that it is easier to read our code.
_make_function = FunctionType
_make_code = CodeType
_make_method = MethodType

# get pyssizet size at runtime by checking against
# the arg parsing typecode.

import ctypes as _ctypes
from weakref import ref as _wref
from ctypes import py_object as _py_object, pythonapi as _pythonapi
from _ctypes import sizeof as _csizeof, Py_INCREF as _Py_INCREF
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


def _getref(ob):
    return _Py_ssize_t.from_address(id(ob)).value


_PyHack_SetItem = _pythonapi.PyStructSequence_SetItem


# cache to store list of weak references. We need this so that
# the weak ref object itself stays alive so that the callback can
# be called. In Python 3.4 we can just use weakref.finalize instead.

_hack_cache = set()


def _hack_callback(hackref):
    """

    Execute the cleanup action by the function hack weakref.
    Because the weakref callback can never be called until func's refcount
    is 0, we should NOT call Py_DECREF on the target index, or even access it
    to check, or we will segfault.

    But, we can be reasonably sure that the refcount is zero, so we can
     override that item. We don't have to worry about Py_DECREF being called
     on an undefined object because of our shoice of function, but if the C API
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

        self = _wref.__new__(cls, func, _hack_callback)
        self.ref_cb = _hack_callback
        self.f_addr = id(func)
        self.f_const = f_consts
        self.f_index = f_index
        return self

    # noinspection PyUnusedLocal
    def __init__(self, func, f_consts, f_index):
        super().__init__(func, self.ref_cb)


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

    # Note: PyTuple_SetItem calls XDECREF on the previous item
    # PyStructSequence_SetItem DOES NOT (which is what is used here)
    #
    _PyHack_SetItem(pyob_ob, pyob_i, pyob_newitem)


def _hack_recursive_func(new_func, old_func):
    """

    Hack the recursive function to contain a constant reference
    to itself.

    1) Use low-level capi (via _tuple_set_item) to mutate the co_consts
     tuple object of the function to contain a constant self-reference.
     Set the 'incref' parameter to false, as otherwise the memory would be
     leaked (as there would be no way to decrease the final reference).

    2) Set up a custom weak reference scheme that allows us to keep a
    strong reference to the co_consts tuple, with a callback called when
    the function is deleted.

    3) With function deleted, we now have a tuple with an invald reference,
    but we know which index contains that reference. Use capi again to
    quietly re-write the tuple index to contain Py_None, then delete
    the local tuple reference. See _hack_callback for the function code

    @param new_func: new function
    @type new_func: FunctionType | MethodType
    @param old_func: old function
    @type old_func: FunctionType | MethodType
    @return: None
    @rtype: None
    """

    co_consts = new_func.__code__.co_consts
    co_index = co_consts.index(old_func)

    # Hack the tuple to set up weakref callback scheme
    _tuple_set_item(co_consts, co_index, new_func)
    hackref = _FuncHackRef(new_func, co_consts, co_index)
    _hack_cache.add(hackref)


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
    return _make_code(co.co_argcount, co.co_kwonlyargcount, co.co_nlocals,
                     co.co_stacksize, co.co_flags, bytes(newcode),
                     tuple(newconsts), co.co_names, co.co_varnames,
                     co.co_filename, co.co_name, co.co_firstlineno,
                     co.co_lnotab, co.co_freevars, co.co_cellvars)


def function_maker(old_func, new_code):
    return _make_function(new_code, old_func.__globals__, old_func.__name__, old_func.__defaults__, old_func.__closure__)


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
    func_repr = "<%s.%s>" % (mod, name)
    ob_repr = object.__repr__

    if verbose:
        print("Attempting to optimize %s." % func_repr)

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
            # todo: Extended arg: get oparg, shift << 16, i += 3, add oparg to NEXT oparg value of NEXT op, see inspect module
            return f

        if op == LOAD_GLOBAL:

            # Each oparg is an unsigned byte in range (0, 255).
            # If the size of co_consts is > 255, overflow would be stored
            # in newcode[i + 2] (or more, with EXTENDED_ARG).
            # Bit shift and add together.
            # See ceval.c or inspect module for OPARG math

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

                    if verbose:
                        print("Making new constant %s for function %s" % (ob_repr(value), func_repr))

                # Bitwise & 0xff, shift >> 8: bytes have max capacity of 255
                # use bit twiddling to store multibyte int into two bytes.
                # See ceval.c or inspect module for OPARG math.

                newcode[i] = LOAD_CONST
                newcode[i + 1] = pos & 0xff
                newcode[i + 2] = pos >> 8

        i += 1
        if op > GREATER_HAVE_ARG:
            i += 2

    if not changed:
        if verbose:
            print("No load globals found- returning unmodified function %s." % func_repr)
        return f

    # Make code object from type of code in case there
    # is a difference between FunctionType, MethodType, etc

    f_code = code_maker(co, newcode, newconsts)
    new_func = function_maker(f, f_code)

    if type(f) is MethodType:
        new_func = _make_method(new_func, f.__self__)

    if f in new_func.__code__.co_consts:
        if verbose:
            print("Recursive function detected!")
            print("Hacking recursive function %s!" % func_repr)
        _hack_recursive_func(new_func, f)

    if verbose:
        print("Returning improved function %s" % func_repr)

    return new_func


#========================================================================
# Binding functions
#========================================================================


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


def bind_all(ns, env=None, blacklist=None, verbose=False, **kwargs):
    """
    Bind all functions in a namespace using make_constants
    @param ns: namespace
    @type ns: dict
    @return: None (mutate in place)
    @rtype: None
    """

    # use the same wrapper for all functions:
    wrapper = make_constants(env, blacklist, verbose, **kwargs)

    # make sure dict is not modified during iteration!
    items = tuple(ns.items())

    for k, v in items:
        if type(v) in (FunctionType, MethodType):
            ns[k] = wrapper(v)


class ConstantOptimizingMeta(type):
    def __new__(mcs, name, bases, namespace):
        """

        Meta to optimize the class's functions to use constant
        global lookups.

        @param mcs: metaclass
        @type mcs: T
        @param name: class name
        @type name: str
        @param bases: bases tuple
        @type bases: tuple
        @param namespace: namespace
        @type namespace: dict
        @return: type
        @rtype: ConstantOptimizingMeta
        """

        env = namespace.pop('__env__', None)
        if env is not None:
            pass  # Todo
        else:
            return type.__new__(mcs, name, bases, namespace)
