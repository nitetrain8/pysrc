"""

Created by: Nathan Starkweather
Created on: 03/29/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'

from opcode import opmap, HAVE_ARGUMENT, EXTENDED_ARG

LOAD_CONST = opmap['LOAD_CONST']
STORE_GLOBAL = opmap['STORE_GLOBAL']
LOAD_GLOBAL = opmap['LOAD_GLOBAL']


def _make_constants(f, env=None):
    """
    My implementation of make-constants function. Yay!.

    Original: http://code.activestate.com/recipes/576904/

    @param f:
    @type f:
    @return:
    @rtype:
    """

    co = f.__code__
    newcode = list(co.co_code)
    co_names = co.co_names
    newconsts = list(co.co_consts)
    newconsts_append = newconsts.append

    import builtins

    if env is None:
        env = {}
    env.update(vars(builtins))

    env_get = env.get

    codelen = len(newcode)
    i = 0
    while i < codelen:
        op = newcode[i]

        if op in (EXTENDED_ARG, STORE_GLOBAL):
            # todo: store-global can be worked around with a double pass
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
                for pos, v in enumerate(newconsts):
                    if v is value:
                        break
                else:
                    pos = len(newconsts)
                    newconsts_append(value)

                # Bitwise and, by 0xff, shift >> 8: if position is > 255,
                # first arg should be max of 255, and second
                # arg should have the carryover

                newcode[i] = LOAD_CONST
                newcode[i + 1] = pos & 0xff
                newcode[i + 2] = pos >> 8

        i += 1
        if op >= HAVE_ARGUMENT:
            i += 2

    # Make code object from type of code in case there
    # is a difference between FunctionType, MethodType, etc

    make_code = type(co)
    make_function = type(f)
    from typehint import Code as make_code
    f_code = make_code(co.co_argcount, co.co_kwonlyargcount, co.co_nlocals, co.co_stacksize, co.co_flags, bytes(newcode),
                  tuple(newconsts), co.co_names, co.co_varnames, co.co_filename, co.co_name, co.co_firstlineno,
                  co.co_lnotab, co.co_freevars, co.co_cellvars)

