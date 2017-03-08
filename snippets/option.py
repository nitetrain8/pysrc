import json

class OptionCategory():
    def __iter__(self):
        d = self.__class__.__dict__.copy()
        d.update(self.__dict__)
        ob = ((k, v) for k,v in d.items() if k[0] != "_" and k[-1]!="_")
        return iter(ob)
    
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
        object.__setattr__(self, k, v)
        
    def asdict(self):
        basedict = dict(iter(self))
        rv = {}
        for k in basedict:
            v = basedict[k]
            if isinstance(v, OptionCategory):
                v = v.asdict()
            rv[k] = v
        return rv
    
    def jsonify(self, **kw):
        kw['indent'] = kw.get('indent') or 4
        return json.dumps(self.asdict(), **kw)