"""

Created by: Nathan Starkweather
Created on: 03/20/2016
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'

import logging

logger = logging.getLogger(__name__)
_h = logging.StreamHandler()
_f = logging.Formatter("%(created)s %(name)s %(levelname)s (%(lineno)s): %(message)s")
_h.setFormatter(_f)
logger.addHandler(_h)
logger.propagate = False
logger.setLevel(logging.DEBUG)
del _h, _f
import sys


import numpy as np


class RingBuffer():
    """ Numpy-based ring buffer """

    def __init__(self, maxsize, dtype=np.float32):
        if not maxsize or maxsize < 0:
            raise ValueError("%s requires max size argument" % self.__class__.__name__)
        self._queue = np.zeros(maxsize, dtype)
        self._dtype = dtype
        self._maxsize = maxsize
        self._end = 0
        self._sz = 0

    def put(self, d):
        self._queue[self._end] = d
        self._end += 1
        if self._end == self._maxsize:
            self._end = 0
        if self._sz < self._maxsize:
            self._sz += 1

    def put_list(self, lst):
        """
        :param lst: list to extend data from
        :type lst: list | tuple | np.ndarray
        """
        slen = len(lst)
        if slen > self._maxsize:
            raise ValueError("Can't add more than maxsize elements (%d > %d)" % (slen, self._maxsize))
        if slen + self._end <= self._maxsize:
            start = self._end
            end = slen + self._end
            self._queue[start:end] = lst
            self._end = end
        else:
            # add slice in two steps
            first_step = self._maxsize - self._end
            self._queue[self._end: self._maxsize] = lst[:first_step]
            second_step = slen - first_step
            self._queue[:second_step] = lst[first_step:]
            self._end = second_step

        if self._sz < self._maxsize:
            self._sz += slen
        if self._end == self._maxsize:
            self._end = 0

    def extend(self, it):
        try:
            it.__len__  # list, tuple, nparray
        except AttributeError:
            it = tuple(it)
        self.put_list(it)

    def get(self):
        """
        Get method. Returns the entire queue but does NOT
        drain the queue.
        """
        if self._sz < self._maxsize:
            return self._queue[: self._end]
        else:
            return np.roll(self._queue, -self._end)

    def __len__(self):
        return self._sz

    def clear(self):
        self._end = 0
        self._sz = 0


class InfiniteBuffer():

    def __init__(self, iterable=None, dtype=np.float32, initial_size=1000):
        self.empty_sz = sys.getsizeof(np.arange(0, dtype=dtype))
        remaining = 4096 - self.empty_sz
        self._itemsize = dtype().itemsize
        assert not (remaining % self._itemsize)
        initial = remaining // self._itemsize
        item_per_pg, zero = divmod(4096, self._itemsize)
        assert zero == 0
        if initial < initial_size:
            extra, mod = divmod(initial_size - initial, item_per_pg)
            initial += extra * item_per_pg
            if mod:
                initial += item_per_pg
        assert (self.empty_sz + initial * self._itemsize) % 4096 == 0

        self._queue = np.zeros(initial, dtype=dtype)
        self._index = 0
        self._sz = len(self._queue)
        assert self._sz == initial
        self._item_per_pg = item_per_pg

        if iterable is not None:
            self.extend(iterable)

    def clear(self):
        self._index = 0

    def __len__(self):
        return self._index

    def _grow(self, pages=1):
        added = self._item_per_pg * pages
        newsz = self._sz + added
        self._queue = np.concatenate((self._queue, np.zeros(added, dtype=self._queue.dtype)))
        self._sz = newsz

    def append(self, item):
        if self._index == self._sz:
            self._grow()
        self._queue[self._index] = item
        self._index += 1

    put = append

    def get(self):
        return self._queue[:self._index]

    def extend(self, it):
        try:
            lit = len(it)
        except TypeError:  # no __len__
            it = tuple(it)
            lit = len(it)

        end = self._index + lit
        needed = end - self._sz
        if needed > 0:
            pgs_needed = needed // self._item_per_pg + 1
            self._grow(pgs_needed)
        self._queue[self._index: end] = it
        self._index = end

