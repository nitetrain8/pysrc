''' This module was made during the proof of concept stage.
It sucks. The whole snippets.metas thing is a mess.

Metaclassing is a mess. Actually, metaclassing is a nice
way of wrapping all class-creation code into one.
Control instance creation behavior in __call__, use __new__
for any modification that is cleaner with direct access
to the class body namespace, and use __init__ in the same
way decorators would normally be used.

In theory, anyway. In practice, there aren't enough classes
being defined to really justify being elaborate, but using an
empty base class to allow metaclass access by subclassing
is a quick and centralized way to turn on/turn off various
meta-behaviors which will be useful during the debugging stage.

'''

from PyQt5.uic.Compiler.compiler import UICompiler

from snippets.metas import OverloadWarningMeta, ManyMetas

# noinspection PyUnresolvedReferences
from snippets.verbose import pfc, VerboseDict
import types


_uimeta = ManyMetas(OverloadWarningMeta, Factory=type(UICompiler))
  

class MyUiCompilerMeta(_uimeta):
    
    def __new__(cls, name, bases, kwargs):  

        # cls.do_local_PFC(name, kwargs)
        
        new_cls = super().__new__(cls, name, bases, kwargs)
        
#         cls.do_mro_PFC(new_cls)
                
        return new_cls
    
    @classmethod
    def do_local_PFC(cls, name, kwargs):
        _callable = cls.isCallableType
        for k,v in kwargs.items():
            if _callable(v):
                kwargs[k] = pfc(v)
                
    @classmethod     
    def do_mro_PFC(cls, new_cls):
        _callable = cls.isCallableType
        for parent in new_cls.__mro__:
            for k,v in parent.__dict__.items():
                if _callable(v):
                    setattr(parent, k, pfc(v))
    
    @staticmethod
    def isCallableType(attr):
            return isinstance(attr, types.FunctionType) or \
                isinstance(attr, types.MethodType)
                
    # @classmethod
    # def __prepare__(cls, *args):
    #     return VerboseDict()


class MyUiBase(UICompiler, metaclass=MyUiCompilerMeta):
    pass


