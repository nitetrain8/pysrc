


class myklass():
    @property
    def foo(self):
        print("foo!")
        return "bar"


mylist = list(str(i) for i in range(10))

m = myklass()

print(m.foo.join(mylist))

