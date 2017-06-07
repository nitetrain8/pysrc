import json
from collections import OrderedDict
import types

_FUNC = (types.FunctionType, types.MethodType)

class OptionMeta(type):
    def __new__(mcs, name, bases, kw):
        fields = []
        fields.extend(k for k in kw if not isinstance(kw[k], _FUNC) and k not in {"__qualname__", "__module__"})
        kw['_fields_'] = fields
        return type.__new__(mcs, name, bases, kw)
        
    def __prepare__(self, bases):
        return OrderedDict()


class OptionCategory(metaclass=OptionMeta):
    def __iter__(self):
        cd = self.__class__.__dict__
        sd = self.__dict__
        rv = []
        for f in self._fields_:
            if f[0] == "_" or f[-1] == "_": continue
            try:
                v = sd[f]
            except KeyError:
                v = cd[f]
            rv.append((f, v))
        return iter(rv)
    
    def __repr__(self):
        buf = []
        for k, v in self:
            if isinstance(v, OptionCategory):
                v = "<More Options...>"
            buf.append("%s: %s" %(k,v))
        return "\n".join(buf)
    
    def __init__(self):
        self.__dict__.update(self.__class__.__dict__)
    
    def __setattr__(self, k, v):
        if k not in self.__dict__:
            raise AttributeError(k)
        elif k == "_fields_":
            raise AttributeError("Can't set _fields_ property")
        object.__setattr__(self, k, v)
        
    def asdict(self):
        rv = OrderedDict()
        for k in self._fields_:
            v = getattr(self, k)
            if isinstance(v, OptionCategory):
                v = v.asdict()
            rv[k] = v
        return rv
    
    def jsonify(self, **kw):
        kw['indent'] = kw.get('indent') or 4
        return json.dumps(self.asdict(), **kw)
    
    def pretty_string(self, expand=False, indent=0):
        buf = []
        ind = indent * "    "
        for k, v in self:
            if isinstance(v, OptionCategory):
                if expand:
                    s = "\n" + v.pretty_string(expand, indent+1)
                else:
                    s = "<More Options...>"
            else:
                s = str(v)
            buf.append("%s%s: %s" %(ind, k,s))
        return "\n".join(buf)

    def __repr__(self):
        return self.pretty_string(False, 0)