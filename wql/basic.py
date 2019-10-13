import datetime

def _ts2dt(t):
    return datetime.datetime.fromtimestamp(t/1000)

def _erepr(s, *a):
    if a:
        s2 = ": " + ", ".join("%r"%r for r in a)
    else:
        s2 = ""
    return "<%s%s>"%(s.__class__.__name__, s2)


class BaseModel():

    def __init__(self, api):
        self.api = api

    def __str__(self):
        return _erepr(self, *(getattr(self, attr) for attr in self._repr_attr_))


class Collection(BaseModel):
    _fast_lookup_ = []

    def __init__(self, api, l):
        self._list = list(l)
        self._fld = {}
        for attr in self._fast_lookup_:
            self._fld[attr] = {getattr(ob, attr): ob for ob in self._list}
        
    def __getitem__(self, key):
        for a in self._fast_lookup_:
            d = self._fld[a]
            try:
                return d[key]
            except KeyError:
                pass
        raise KeyError("%r not found" % key)

