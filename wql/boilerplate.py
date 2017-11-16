# Generate classes and containers for models from specified data
# I prefer to do it this way rather than dynamically create the whole
# thing at runtime each time it starts up. 

def funcify(e):
    a, f = e
    if f is None:
        return "%s = %s" % (a,a)
    else:
        return "%s = %s(%s)"%(a, f, a)


class SimpleData():
    def __init__(self, name, extract, repr_attr, base="BaseModel"):
        self.name = name
        self.extract = extract
        self.base = base
        self.repr_attr = repr_attr

    def tostring(self):
        init_args = [e[0] for e in extract]
        init_argstr = ", ".join("%s=None"%a for a in init_args)
        apply_attrstr = "\n       ".join("self.%s" % funcify(e) for e in self.extract)
        comma = ", " if init_args else ""
        selfattrstr = ""
        src = """
class %s(%s):
    def __init__(self, api%s%s):
        super().__init__(api)
        %s

    def _from_list(self, l):
        cls = self.__class__
        self2 = cls(self.api%s%s)

""" % (
            self.name, 
            self.base, 
            comma,
            init_argstr,
            apply_attrstr
            )

def Collection():