"""

Created by: Nathan Starkweather
Created on: 03/29/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'

__all__ = [
            'make_constants',
            'optimize_namespace',
            'ConstantOptimizingMeta',
            'ConstantGlobals',
            'make_constants_class'
            ]

from opcode import opmap, HAVE_ARGUMENT, EXTENDED_ARG, opname
from types import FunctionType, CodeType, MethodType

# hack methods
from ._ctypes_hax import _tuple_set_item, _add_function_hack

LOAD_CONST = opmap['LOAD_CONST']
STORE_GLOBAL = opmap['STORE_GLOBAL']
LOAD_GLOBAL = opmap['LOAD_GLOBAL']
GREATER_HAVE_ARG = HAVE_ARGUMENT + 1


# The type constructors actually do the work, but
# providing aliases here so that it is easier to read our code.
_make_function = FunctionType
_make_code = CodeType
_make_method = MethodType


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
    the local tuple reference. See _func_hack_callback for the function code

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
    _add_function_hack(new_func, co_consts, co_index)


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


def getops(codestr):
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


def _code_maker(co, newcode, newconsts):
    return _make_code(co.co_argcount, co.co_kwonlyargcount, co.co_nlocals,
                     co.co_stacksize, co.co_flags, bytes(newcode),
                     tuple(newconsts), co.co_names, co.co_varnames,
                     co.co_filename, co.co_name, co.co_firstlineno,
                     co.co_lnotab, co.co_freevars, co.co_cellvars)


def _function_maker(old_func, new_code):
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

    f_code = _code_maker(co, newcode, newconsts)
    new_func = _function_maker(f, f_code)

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


def make_constants(env=None, blacklist=None, verbose=False, use_builtins=True, **kwargs):
    """

    Function Decorator.

    Public interface to _make_constant_globals. Use env=globals() to grab everything,
    use blacklist to ban things. Pass arbitrary args to kwargs for convenience of not having
    to make a new mapping for each dict.

    @param env: pass in a dict mapping names <=> values to override. Caller
                responsible for ensuring that names map to the correct value.
    @type env: dict
    @type blacklist: dict | None
    @type verbose: bool
    @param kwargs:
    @return: make_constants function wrapper
    @rtype: types.FunctionType
    """
    if use_builtins:
        import builtins
    else:
        builtins = {}  # dummy

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


def optimize_namespace(ns, env=None, blacklist=None, verbose=False, use_builtins=True, **kwargs):
    """
    Bind all functions in a namespace using make_constants
    @param ns: namespace
    @type ns: dict
    @return: None (mutate in place)
    @rtype: None
    """

    # use the same wrapper for all functions:
    wrapper = make_constants(env, blacklist, verbose, use_builtins, **kwargs)

    # make sure dict is not modified during iteration!
    items = tuple(ns.items())

    for k, v in items:
        if type(v) in (FunctionType, MethodType):
            ns[k] = wrapper(v)


class ConstantOptimizingMeta(type):
    def __new__(mcs, name, bases, namespace):
        """

        Meta to optimize the class's functions to use constant
        global lookups. Set a class attribute __env__ to add stuff
        to namespace.

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

        #: @type: dict
        env = namespace.pop('__env__', {})
        if env is not None:
            optimize_namespace(namespace, env)
        return type.__new__(mcs, name, bases, namespace)


class ConstantGlobals(metaclass=ConstantOptimizingMeta):
    """ Get optimizing behavior by superclass instead of metaclass. """
    pass


def make_constants_class(env=None, blacklist=None, verbose=False, use_builtins=True, **kwargs):
    """
    Class decorator for binding stuff.
    """
    def class_wrapper(cls):
        optimize_namespace(cls.__dict__, env, blacklist, verbose, use_builtins, **kwargs)
        return cls
    return class_wrapper
