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

make_function = FunctionType
make_code = CodeType
make_method = MethodType


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

    if verbose:
        print("Attempting to optimize", f.__name__)

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

    f_code = make_code(co.co_argcount, co.co_kwonlyargcount, co.co_nlocals,
                       co.co_stacksize, co.co_flags, bytes(newcode),
                       tuple(newconsts), co.co_names, co.co_varnames,
                       co.co_filename, co.co_name, co.co_firstlineno,
                       co.co_lnotab, co.co_freevars, co.co_cellvars)

    new_func = make_function(f_code, f.__globals__, f.__name__, f.__defaults__, f.__closure__)

    if type(f) is MethodType:
        new_func = make_method(new_func, f.__self__)

    return new_func


def make_constants(env=None, blacklist=(), verbose=False, **kwargs):
    """
    public interface to _make_constant_globals, for sake of accepting whitelist
    in the form of kwargs
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
        pop = real_env.pop
        if verbose:
            sentinel = object()
            for key in blacklist:
                if pop(key, sentinel) is not sentinel:
                    print("Removing %s from env for function <%s>" % (key, f.__name__))
        else:
            for key in blacklist:
                pop(key, None)

        return _make_constant_globals(f, env, verbose)

    return constants_wrapper()




