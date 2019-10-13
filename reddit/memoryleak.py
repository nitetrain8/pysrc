"""

Created by: Nathan Starkweather
Created on: 02/15/2014
Created in: PyCharm Community Edition


"""

from weakref import ref as wref

class Link():
    count = 0
    def __new__(cls):
        cls.count += 1
        return super().__new__(cls)
    def __init__(self):
        self.inum = self.count
        self.next = None
        self.prev = None
    #
    def __del__(self):
        print("link %d deleted!" % self.inum)


def dead(obj):
    print("obj is dead!")

def make_list():
    start = Link()
    last = start
    start.next = start
    start.prev = None
    for i in range(10):
        next = Link()
        last.next = next
        next.prev = wref(last, dead)
        last = next

    last.next = start
    start.prev = wref(last, dead)

    i = start.next
    id_start = id(start)
    del start
    del last
    del next

    while id(i) != id_start:
        print("next link")
        prev = i
        i = i.next
        # prev.next = None

    return None

def make_list2():
    mylist = [Link() for i in range(10)]
    mylist2 = [wref(l, dead) for l in mylist]
    return mylist2

def make_list3():
    mydict = {i : Link() for i in range(10)}
    mylist = [wref(v, dead) for v in mydict.values()]
    return mylist
make_list()
input("1")
a = make_list2()
input("2")
b = make_list3()
input("3")

