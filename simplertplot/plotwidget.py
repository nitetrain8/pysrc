"""

Created by: Nathan Starkweather
Created on: 04/16/2016
Created in: PyCharm Community Edition


"""
import itertools
from matplotlib.backends import backend_tkagg
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.ticker import NullFormatter, NullLocator, FormatStrFormatter
from matplotlib.transforms import Bbox

import tkinter as tk
from . import queues

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



class PlotWidgetError(Exception):
    pass


class _PlotWidgetFigManager(FigureManagerBase):
    pass

class PlotWidgetTkAgg(backend_tkagg.FigureCanvasTkAgg):
    def resize(self, event):
        super().resize(event)
        self._w.resize(event)


class RTPlotWidget():
    _fig_counter = itertools.count(1)

    # __slots__ = 'frame', 'master', 'num', 'figmanager', 'figure', \
    #             'figcanvas', 'subplot', 'line', 'renderer', 'x_data', \
    #             'y_data', 'tkcanvas', 'background', 'xaxis', 'yaxis', 'all_bbox', \
    #             '_setup', 'xlabel', 'ylabel', "title_text"

    def __init__(self, master, max_pts=1000):
        self.master = master
        self.num = next(self._fig_counter)
        self.figmanager = None
        self.figure = None
        self.figcanvas = None
        self.subplot = None
        self.line = None
        self.renderer = None
        self.xaxis = None
        self.yaxis = None
        self.tkcanvas = None
        self.background = None
        self.all_bbox = None

        if max_pts is None:
            self.x_data = queues.InfiniteBuffer()
            self.y_data = queues.InfiniteBuffer()
        else:
            self.x_data = queues.RingBuffer(max_pts)
            self.y_data = queues.RingBuffer(max_pts)
        self.max_pts = max_pts
        self.setup()

    def _cache_background(self, bbox):

        xaxis = self.xaxis
        yaxis = self.yaxis

        # cache formatters & locators
        xmjf = xaxis.get_major_formatter()
        xmjl = xaxis.get_major_locator()
        ymjf = yaxis.get_major_formatter()
        ymjl = yaxis.get_major_locator()

        # set null placeholders
        xaxis.set_major_formatter(NullFormatter())
        xaxis.set_major_locator(NullLocator())
        yaxis.set_major_formatter(NullFormatter())
        yaxis.set_major_locator(NullLocator())

        # cache background
        self.figcanvas.draw()
        background = self.figure.canvas.copy_from_bbox(bbox)

        # restore
        xaxis.set_major_formatter(xmjf)
        xaxis.set_major_locator(xmjl)
        yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
        yaxis.set_major_locator(ymjl)

        self.background = background

    def create_figure(self, figsize=(4, 2), dpi=None, facecolor=None,
                      edgecolor=None, linewidth=0.0, frameon=None,
                      subplotpars=None, tight_layout=None):
        """ Create an ordinary matplotlib figure. """
        if self.figure:
            raise PlotWidgetError("Cannot override existing figure.")
        f = backend_tkagg.Figure(figsize, dpi, facecolor, edgecolor, linewidth, frameon, subplotpars, tight_layout)
        self.figure = f
        return f

    def setup(self):
        if self.figure is None:
            self.create_figure()

        if self.subplot is None:
            self.create_subplot(1, 1, 1)

        # Explicitly named to avoid confusion later
        self.figcanvas = PlotWidgetTkAgg(self.figure, self.master)
        self.tkcanvas = self.figcanvas._tkcanvas
        self.figmanager = _PlotWidgetFigManager(self.figcanvas, self.num)
        self.figcanvas._w = self

        self.renderer = self.figcanvas.get_renderer()

        self.xaxis = self.subplot.xaxis
        self.yaxis = self.subplot.yaxis

        self.all_bbox = self._calculate_bbox()

        self.xlabel = self.xaxis.get_label()
        self.ylabel = self.yaxis.get_label()
        self.title_text = self.subplot.title

        self.figure.subplots_adjust(top=0.9, left=0.15, bottom=0.15)
        self._cache_background(self.all_bbox)

        # this line must come after background is cached
        self.line, = self.subplot.plot(self.x_data.get(), self.y_data.get())

    def resize(self, event):
        self.figcanvas.draw()
        self._handle_text_update()

    def _calculate_bbox(self):
        r = self.renderer
        bboxes = self.xaxis.get_window_extent(r), self.yaxis.get_window_extent(r), self.subplot.bbox
        all_bbox = Bbox.union(bboxes)
        (x0, y0), (x1, y1) = all_bbox.get_points()
        w = x1 - x0
        h = y1 - y0
        all_bbox = Bbox.from_bounds(x0, y0, w * 1.02, h * 1.02)
        return all_bbox

    def format(self, title=None, xaxis=None, yaxis=None):
        if title is not None:
            self.set_title_text(title)
        if xaxis is not None:
            self.set_xaxis_text(xaxis)
        if yaxis is not None:
            self.set_yaxis_text(yaxis)

    def _handle_text_update(self):
        self.figcanvas.draw()
        self.all_bbox = self._calculate_bbox()
        lines = self.subplot.lines[:]
        self.subplot.lines = []
        self._cache_background(self.all_bbox)
        self.subplot.lines = lines
        self.renderer = self.figcanvas.get_renderer()
        self._update_data()

    def set_xaxis(self, **kw):
        self.xlabel.set(**kw)
        self._handle_text_update()

    def set_xaxis_text(self, s):
        self.xlabel.set_text(s)
        self._handle_text_update()

    def set_yaxis(self, **kw):
        self.ylabel.set(**kw)
        self._handle_text_update()

    def set_yaxis_text(self, s):
        self.ylabel.set_text(s)
        self._handle_text_update()

    def set_title_text(self, s):
        self.title_text.set_text(s)
        self._handle_text_update()

    def create_subplot(self, *args, **kw):
        if self.subplot:
            raise PlotWidgetError("Cannot override existing subplot")
        self.subplot = self.figure.add_subplot(*args, **kw)
        return self.subplot

    def grid(self, **kw):
        self.tkcanvas.grid(**kw)

    def pack(self, fill=tk.BOTH, expand=True, side=tk.TOP, **kw):
        kw['fill'] = fill
        kw['expand'] = expand
        kw['side'] = side
        self.tkcanvas.pack(**kw)

    def pack_forget(self):
        self.tkcanvas.pack_forget()

    def set_data(self, x, y):
        self.x_data.clear()
        self.y_data.clear()
        self.x_data.extend(x)
        self.y_data.extend(y)
        self._update_data()

    def reset(self):
        self.x_data.clear()
        self.y_data.clear()
        self._update_data()

    clear = reset

    def extend_xy(self, x, y):
        self.x_data.extend(x)
        self.y_data.extend(y)
        self._update_data()

    def add_xy(self, x, y):
        self.x_data.put(x)
        self.y_data.put(y)
        self._update_data()

    def _update_data(self):
        self.line.set_data(self.x_data.get(), self.y_data.get())
        self.subplot.relim()
        self.subplot.autoscale_view(True, True, True)
        lower, upper = self.subplot.get_ybound()
        self.subplot.set_ylim(lower, upper + (upper - lower) * 0.02, True, None)
        self._update()

    def _update(self):
        # self.figcanvas.restore_region(self.background)
        # r = self.renderer
        # self.xaxis.draw(r)
        # self.yaxis.draw(r)
        # self.line.draw(r)
        # self.figcanvas.blit(self.all_bbox)
        self.figcanvas.draw()

