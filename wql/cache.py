import collections

class URLCache():
    def __init__(self, history=200):
        self._cache = {}
        self._history = collections.deque(maxlen=history)

    def check(self, v):
        return v in self._cache

    def get(self, v):
        return self._cache.get(v)

    def save(self, u, v):
        self._cache[u] = v
        self._history.append(u)

    def uncache(self):
        try:
            u = self._history.pop()
        except IndexError:
            return
        try:
            del self._cache[u]
        except KeyError:
            return

    def clear(self):
        self._cache.clear()
        self._history.clear()
