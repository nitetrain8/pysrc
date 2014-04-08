from _ctypes import *
from ctypes import *
from weakref import *


def cb(o):
    print("object deleted!")
    print(o.hack)
    # print(o.hack_index)
    # print(o.hack[o.hack_index])


class HaxRef(ref):
    def __new__(cls, ob, callback):
        self = ref.__new__(cls, ob, callback)
        self.hack = ob.__code__.co_consts
        # self.hack_index = self.hack.index(ob)
        return self


def foo():
    a = 1
    b = 2
    c = 3


HaxRef(foo, cb)
import sys
del foo
sys.stdout.flush()
# input('')

# from pysrc.snippets.optimize_constants import hack_tuple
#
# tpl = foo.__code__.co_consts
# print(c_uint32.from_address(id(foo)))
# hack_tuple(tpl, 2, foo, False)
# tpl_addr = id(tpl)
# tpl_ptr = c_uint32.from_address(tpl_addr)
# print(tpl_ptr.value)
#
# del tpl
# print(c_uint32.from_address(id(foo)))
# HaxRef(foo, cb)
# ptr = c_uint32.from_address(id(foo))
# del foo
# print(tpl_ptr.value)
# print(ptr.value)
# # print(c_uint32.from_address(id(foo)))

