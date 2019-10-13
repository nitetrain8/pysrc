"""

Created by: Nathan Starkweather
Created on: 01/13/2016
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'

import tkinter as tk
import tkinter.ttk as ttk

from pysrc import logger

_logger = logger.BuiltinLogger(__name__)
_info = _logger.info
_debug = _logger.debug


class SimpleMenu(ttk.OptionMenu):
    def __init__(self, master, command, initvalue, options):
        self.var = tk.StringVar(None, initvalue)
        ttk.OptionMenu.__init__(self, master, self.var, None, command=command, *options)

    def get(self):
        return self.var.get()

    def grid(self, row, col, **kw):
        ttk.OptionMenu.grid(self, row=row, column=col, **kw)


class ItemButton(ttk.Button):
    def __init__(self, master, name, cmd, **kw):
        self.tv = tk.StringVar(None, name)
        super().__init__(master, textvariable=self.tv, command=cmd, **kw)

    def grid(self, row, col, **kwargs):
        super().grid(row=row, column=col, **kwargs)


class StatefulItemButton(ItemButton):
    def __init__(self, master, name, initial_cmd, **kw):
        super().__init__(master, name, self._do_cmd, **kw)
        self._cmd = initial_cmd

    def _do_cmd(self, *args, **kwargs):
        self._cmd(*args, **kwargs)

    def set_cmd(self, cmd):
        self._cmd = cmd


class SimpleEntryButton():
    def __init__(self, root, frame_text, button_text, button_cmd):
        self.frame = ttk.Frame(root)
        self.label = ttk.Label(self.frame, text=frame_text)
        self.entry_tv = tk.StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.entry_tv)
        self.button = StatefulItemButton(self.frame, button_text, button_cmd)

    def grid(self, row, col):
        self.frame.grid(row=row, column=col, rowspan=2, sticky=tk.N)
        self.entry.grid(row=1, column=1, columnspan=1)
        self.button.grid(1, 2)
        self.label.grid(row=0, column=1, sticky=tk.W)

    def grid_forget(self):
        for w in (self.frame, self.entry, self.button, self.label):
            w.grid_forget()

    def get_entry_text(self):
        return self.entry_tv.get()


class SimpleListbox():
    def __init__(self, root, label_text):
        self.frame = ttk.Frame(root)
        self.label = ttk.Label(root, text=label_text)
        self.listbox = tk.Listbox(root)

    def grid(self, row, col):
        self.frame.grid(row=row, column=col)
        self.label.grid(row=0, column=0)
        self.listbox.grid(row=1, column=0)

    def grid_forget(self):
        for w in (self.frame, self.label, self.listbox):
            w.grid_forget()

    def insert(self, index, items):
        self.listbox.insert(index, *items)

    def delete(self, first, last):
        self.listbox.delete(first, last)

    def clear(self):
        self.delete(0, tk.END)


class SimpleLabelFrame(ttk.LabelFrame):
    def __init__(self, master, text, **kw):
        kw['text'] = text
        ttk.LabelFrame.__init__(self, master, **kw)


class SimpleFrame(ttk.Frame):
    def __init__(self, master, **kw):
        ttk.Frame.__init__(self, master, **kw)
