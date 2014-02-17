
from weakref import ref as wref
class myclass(): pass
a = myclass()
wref(a, lambda x: print("fooing!"))
wref(myclass(), lambda x: print("barring!"))
