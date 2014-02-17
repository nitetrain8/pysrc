"""

Created by: Nathan Starkweather
Created on: 02/15/2014
Created in: PyCharm Community Edition


"""

class Pug():
    def __init__(self):
        print("New Pug!")
    def snort(self):
        print("pug snort")

obj = Pug()
try:
    obj.snort()
except AttributeError:
    pass

if isinstance(obj, Pug):
    obj.snort()

if obj.__class__ is Pug:
    obj.snort()

print(type(obj) == Pug)


    class Dog():
        def bark(self):
            print("dog bark")

    class Pug(Dog):
        def snort(self):
            print("pug snort")

    p = Pug()
    p.bark()
    p.snort()
