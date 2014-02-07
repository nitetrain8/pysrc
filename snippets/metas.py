

'''This module is a bizzare collection of metaclasses
I made for fun. Most notable is the way metaclasses are defined.

The following is relevant for function-based metaclasses. I don't know 
yet if class based metaclasses need to be handled differently.

Each metaclass here is actually a pseudo-metaclass, which accepts
the usual trio of (cls, bases, kwargs) [cls = name of class, not class object],
and returns the modified trio instead of calling type. 

This allows them to be compatible with the "ManyMetas" metaclass, 
which accepts an arbitrary length list of metaclasses to call and modify the 
metaclass arguments. ManyMetas calls each meta in order they were added, 
with the call [cls, bases, kwargs = meta(cls, bases, kwargs, ManyMetas=True)]. 
It then calls the factory metaclass to finalize class creation. The factory
defaults to type. 

The "ManyMetas" parameter is added using the "ManyMetafy" decorator, which
converts pseudo-metaclasses into metaclasses which return modified
cls, bases, kwargs if called from ManyMetas, or type(cls, bases, kwargs) if 
used directly as a metaclass. 

Update 1/18/2014:
Holy goddamn hell what a stupid mess this module is. Clever stuff
everywhere, but a goddamn stupid mess. Still, appropriate for collection
in a 'snippets' library, since some of the ideas here are useful,
even if the hilarious and inappropriate use of metaclassing isn't.
'''

from types import FunctionType, MethodType
from copy import deepcopy, copy, name

__all__ = [
            'MakeMutableCopyMeta',
            'ManyMetas',
            'ManyMetafy',
            'EmptyMethodMeta',
            'ManyMetaError',
            'PyQtSlotDefferMeta',
            'OverloadWarningMeta'
           ]


class ManyMetaError(Exception):
    pass


def ManyMetas(*metas, Factory=type):
    '''Each meta in metas is a pseudo metaclass which
    modifies cls, bases, kwargs and returns them. 
    
    Then this meta calls Factory(cls, bases, kwargs)
    and returns it. 
    
    Should be usable for all basic metaclass usages.
    
    Won't be useful for some factory pattern metaclasses
    that use class callables or whatever to return a class
    or instance of a class instead. 
    
    Unless I add a thingy. Update: thingy added.
    
    Factory is the metaclass called to return the finished
    class. Defaults to type. Yay. 
    
    Update 1/6/2014
    innerMeta now a class, renamed ManyMetaWrapper.
    __new__ calls __new__ of factory class, and inherits from it
    but passes factory to __new__, so it doesn't appear as a type. 
    tee hee. 
    
    Making it a class makes it possible to create and cache a ManyMetaWrapper
    to subclass from or use as a single metaclass, rather than ackwardly
    using ManyMetas(...) for each class. 
    '''
    class ManyMetaWrapper(Factory):
        def __new__(cls, name, bases, kwargs, metas=metas):
            '''Since metaclass is passed as an uncalled keyword
            argument, need to construct a custom metaclass
            that accepts the normal metaclass args, and 
            holds record of metas passed during class 
            declaration.'''
            ManyMetaList = []
            try:
                for meta in metas:
                    name, bases, kwargs = meta(name, bases, kwargs, Many=True)
                    ManyMetaList.append((meta.__name__, meta))
            except TypeError:
                raise ManyMetaError("Metaclass got bad args.\nMeta must return cls, bases, kwargs tuple when called from ManyMeta.")
            
            def view_metas(self):
                return tuple(ManyMetaList)
                
            kwargs['_ManyMetaMro'] = property(view_metas)
            
    #         return Factory.__new__(Factory, cls, bases, kwargs)
            return Factory.__new__(cls, name, bases, kwargs)
    ManyMetaWrapper.__name__ = Factory.__name__
    return ManyMetaWrapper


def ManyMetafy(metaFunc):
    '''internally used decorator to allow metaclasses to be
    used directly or indirectly through ManyMetas.
    
    Take a callable which accepts cls, bases, kwargs
    and modifies them and returns modified cls, bases, kwargs.
    
    '''
    
    def WrappedMeta(cls, bases, kwargs, Many=False):
        cls, bases, kwargs = metaFunc(cls, bases, kwargs)
        if Many:
            return cls, bases, kwargs
        else:
            return type(cls, bases, kwargs)
    WrappedMeta.__name__ = metaFunc.__name__
    return WrappedMeta


@ManyMetafy
def MakeMutableCopyMeta(name, bases, kwargs):
    '''Magical metaclass that gives each class
    instance a copy of class variables.
    I don't know why I bothered to make this
    since I only need it for one class.'''

    to_copy = []
    for k, v in kwargs.items():
        try:
            hash(v)  # throw error if mutable
        except TypeError:  # thingy is mutable, make copy
            to_copy.append((k, v))

    old_new = kwargs.get('__new__', None)

    if old_new is None:
        if bases:
            old_new = bases[0].__new__
        else:
            old_new = object.__new__

    def __new__(cls, *args, **kwargs):
        
        try:
            self = old_new(cls, *args, **kwargs)
        except TypeError:
            if old_new is object.__new__:
                self = old_new(cls)
            else:
                raise
        
        for k, v in self._to_copy_:
            try:
                setattr(self, k, deepcopy(v))
            except:
                setattr(self, k, copy(v))

        return self
        
    kwargs.update({
                  '__new__' : __new__,
                  '__oldnew__' : old_new,
                  '_to_copy_' : to_copy
                  })

    return name, bases, kwargs


def __empty():
    pass


def EmptyMethod(method, clsname=""):

    methodname = method.__name__

    def _EmptyWarning(*args, **kwargs):
        print("Non-implemented method <%s.%s> called." % (clsname, methodname))
        # print(args)
        # print(kwargs)
        return method(*args, **kwargs)
    
    return _EmptyWarning


def EmptyMethodMeta(cls, bases, kwargs):
    
    # noinspection PyUnresolvedReferences
    emptycode = __empty.__code__.co_code
    for k, v in kwargs.items():
        if isinstance(v, FunctionType) and v.__code__.co_code == emptycode:
            kwargs[k] = EmptyMethod(v, cls)
    
    return cls, bases, kwargs


def EmptyMethodDecorator(cls):
    ''' Class decorator version of empty
    method metaclass.
    '''

    # noinspection PyUnresolvedReferences
    emptycode = __empty.__code__.co_code
    for k, v in cls.__dict__.items():
        if (isinstance(v, FunctionType) or
                isinstance(v, MethodType)) and \
                v.__code__.co_code == emptycode:
            setattr(cls, k, EmptyMethod(v))
    return cls


# from PyQt5.QtCore import pyqtWrapperType as PyQtMeta
#
#
# class PyQtSlotDefferMeta(PyQtMeta):
#
#     def __new__(mcs, name, bases, kwargs):
#         return super(PyQtSlotDefferMeta, mcs).__new__(mcs, name, bases, kwargs)

ovl_ignore_list = [
    '__doc__',
    '__module__',
    '__init__',
    '__new__'
]


@ManyMetafy
def OverloadWarningMeta(name, bases, kwargs):
    '''
    This function really should be a decorator.
    It would be much neater to use it after class
    creation, once python has determined the __mro__
    attribute.

    @param name: class name
    @type name: str
    @param bases: tuple of bases
    @type bases: tuple
    @param kwargs: class body namespace
    @type kwargs: dict
    @return: name, bases, kwargs
    @rtype: tuple

    Using this as a metaclass isn't very good, because
    it is awkward to try and get info about the class
    from either base.__dict__ or even dir, because
    no access to the MRO without calculating it ourselves.
    Leaving this to exist only for legacy reasons.
    '''
    overload_warning_string = "Overload Warning: <%s.%s> overloads <%s.%s>"
    cls_attrs = set(kwargs).difference(ovl_ignore_list)

    for base in bases:
        same = cls_attrs.intersection(base.__dict__)
        cls_attrs.difference_update(same)  # remove checked from cls_attrs
        for attr in same:
            print(overload_warning_string % (name, attr, base.__qualname__, attr))

    return name, bases, kwargs


def func_line(func):
    return func.__code__.co_firstlineno


def OverloadWarning(cls: type, ignore: list=ovl_ignore_list) -> type:
    ''' Implementation of overload warning as a
    decorator, since that makes more sense.

    '''

    warning = "Overload Warning: <%s.%s.%s> overloads <%s.%s.%s>."
    cls_attrs = set(cls.__dict__).difference(ignore)

    mro = cls.__mro__[1:-1]  # cls is first in mro, object is last in mro- skip both

    for supercls in mro:
        same = cls_attrs.intersection(supercls.__dict__)
        cls_attrs.difference_update(same)
        for attr in same:
            print(warning % (cls.__module__,
                                cls.__qualname__,
                                attr,
                                supercls.__module__,
                                supercls.__qualname__,
                                attr))

    return cls
