import requests
from .cache import URLCache
from urllib.parse import urlencode


def make_query(**kw):
    return "?" + urlencode(kw)

class Api():
    verbose = True
    _api_cache_ = URLCache(200)
    def __init__(self, key):
        self.key = key
        self.sess = requests.Session()
        self.base = "https://www.warcraftlogs.com/v1"
        self.zones_ = None
        
    @property
    def zones(self):
        if self.zones_ is None:
            raw = self.request("/zones")
            self.zones_ = Zones(self, raw)
        return self.zones_
        
    def request(self, path, **kw):
        kw['api_key'] = self.key
        qs = make_query(**kw)
        p2 = path + qs
        url = self.base + p2

        # check cache
        raw = self._api_cache_.get(url)
        if raw is not None:
            return raw

        if self.verbose:
            print("Requesting %r"%p2)
        r = self.sess.get(url)
        r.raise_for_status()
        raw = json.loads(r.content.decode())

        # store cache
        self._api_cache_.save(url, raw)
        
        return raw
    
    def clear_cache(self):
        self._api_cache_.clear()

    def uncache(self):
        # ordered url history is kept as a list,
        # for reasons.
        try:
            u = self._history.pop()
        except IndexError:
            return
        try:
            del self._api_cache_[u]
        except KeyError:
            return
        
    def parses(self, character, server, region="US"):
        path = "/parses/character/%s/%s/%s" % (character, server, region)
        raw = self.request(path)
        return raw
    
    def reports(self, guildname, servername, region="US"):
        path = "/reports/guild/%s/%s/%s"%(guildname, servername, region)
        raw = self.request(path)
        return Reports(self, raw)
    
    def fights(self, code):
        path = "/report/fights/%s"%code
        raw = self.request(path)
        return Fights(self, raw, code)
    
    def events(self, id, start, end, **kw):
        path = "/report/events/%s"%id
        raw = self.request(path, start=start, end=end, **kw)
        return mk_struct(raw)