"""

Created by: Nathan Starkweather
Created on: 04/16/2016
Created in: PyCharm Community Edition


"""
import pytest

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

from pysrc2.simplertplot.plotwidget import RTPlotWidget
from pysrc2.simplertplot.queues import InfiniteBuffer
import tkinter as tk
import numpy as np


def test_plotwidget():
    x = np.arange(100)
    y = x ** 2 + 2 * x + 3

    root = tk.Tk()
    p = RTPlotWidget(root)
    p.set_data(x, y)
    p.grid()
    root.mainloop()


def test_plotwidget_two():
    x = np.linspace(0, 5, 100)
    y = x ** 2 - 2 * x + 3

    x2 = np.linspace(-5, 0, 100)
    y2 = -x2 ** 2 + 2 * x - 3

    root = tk.Tk()
    p = RTPlotWidget(root)
    p.set_data(x, y)
    p.grid(0, 0)

    p2 = RTPlotWidget(root)
    p2.set_data(x2, y2)
    p2.grid(1, 0)
    root.mainloop()


def test_plotwidget_three():
    x = np.linspace(0, 5, 100)
    y = x ** 2 - 2 * x + 3

    root = tk.Tk()
    p = RTPlotWidget(root)
    p.set_data(x, y)
    p.grid(1, 1)

    p2 = RTPlotWidget(root)
    p2.setup()
    p2.grid(2, 1)
    p2.set_yaxis(text="Hello World! Yaxis")
    p2.set_xaxis(text="XAxis")
    p2.set_title_text("MyTitle")
    from matplotlib.transforms import Bbox
    b1 = p2.subplot.title.get_window_extent(p2.renderer)
    b2 = p2.xlabel.get_window_extent(p2.renderer)
    bb = Bbox.union((b1, b2))
    # p2.figure.subplots_adjust(top=0.65, left=0.25)

    wave = sin_wave()

    def add_sin(n=1):
        for _ in range(n):
            nonlocal wave
            p2.add_xy(*next(wave))
        root.after(1, add_sin, n)

    i = 0
    for r in range(4):
        for c in range(3):
            if r in (1, 2) and c == 1:
                continue
            i += 1
            l = tk.Label(root, text="TestLabel %d" % i)
            l.grid(row=r, column=c)

    root.after(0, add_sin, 5)
    root.mainloop()

def test_plotwidget_hello():
    raise pytest.skip("")
    root = tk.Tk()
    import urllib.request
    import json
    from time import time

    def _time(start=time()):
        return int(time()-start)

    def getmainvalues():
        return json.loads(urllib.request.urlopen("http://71.189.82.196:3/webservice/"
                                      "interface/?&call=getmainvalues&json=1").read().
                          decode("ascii").lower())['message']
    ctrls = {}
    controls = ("agitation", "temperature", "ph", "do")
    for i, ctl in enumerate(controls):
        plot = RTPlotWidget(root, 20)
        plot.grid(i, 0)
        plot.set_title_text(ctl)
        ctrls[ctl] = plot

    def do_gmv():
        mv = getmainvalues()
        for ctl, plot in ctrls.items():
            data = mv[ctl]
            t = _time()
            pv = data['pv']
            plot.add_xy(t, pv)
        root.after(1, do_gmv)
    do_gmv()
    root.mainloop()



from math import sin


def sin_wave(step=0.1):
    x = 0
    while True:
        x += step
        y = sin(x)
        yield x, y



if __name__ == '__main__':
    pytest.main()
