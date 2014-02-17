"""

Created by: Nathan Starkweather
Created on: 02/15/2014
Created in: PyCharm Community Edition


"""
#
# class MyClass():
#     def __init__(self, val):
#         self._val = val
#
#     @property
#     def Val(self):
#         self._val += 1
#         return self._val
#
#     @Val.setter
#     def Val(self, new_val):
#         print("Value changed!")
#         self._val = new_val
#
# m = MyClass(5)
# print(m.Val)
# print(m.Val)
#
# m.Val = 5


    class Imposter(type):
        def __call__(cls, obj, new_value):

            new_name = '_'.join((cls.__name__, type(obj).__name__))
            kwargs = dict(type(obj).__dict__)
            kwargs.update(cls.__dict__)
            imposter = type(new_name, (type(obj),), kwargs)
            new_imposter = imposter.__new__(imposter, new_value)
            new_imposter.__init__(new_imposter, new_value)
            return new_imposter

    class MyClass(metaclass=Imposter):
        def foo(self):
            print("foo")

    m = MyClass("", "foo")
    print(m)
    print(m == "foo")
    m.foo()
    print(m.upper())

    if hasattr(obj, 'bark'):
        obj.bark()
