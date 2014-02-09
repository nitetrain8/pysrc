__author__ = 'Nathan Starkweather'
'''

Created by: Nathan Starkweather
Created on: 02/06/2014
Created in: PyCharm Community Edition


'''
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QListView
from collections import OrderedDict


class StringListModel(QStringListModel):

    """
    String List Model subclass to more easily
    wrap the process of adding and removing strings.
    """
    def __init__(self, *args):
        super().__init__(*args)

    def appendString(self, qstr: str) -> None:
        row = self.rowCount()
        self.insertRows(row, 1)
        index = self.index(row)
        self.setData(index, qstr)

    def removeString(self, qstr: str) -> None:
        row = self.stringList().index(qstr)
        self.removeRows(row, 1)


class _UniqueStrError(ValueError):
    """ Imposter ValueError with pre-defined
    Error message
    """
    def __new__(cls, string: str) -> ValueError:
        msg = "Error: %s already exists in list." % string
        return ValueError.__new__(ValueError, msg)


class UniqueStringListModel(StringListModel):
    """ String List subclass that only
    allows unique strings.
    """
    _removeString = StringListModel.removeString
    _setStringList = QStringListModel.setStringList

    def __init__(self, *args):
        super().__init__(*args)

    def setStringList(self, strings: list) -> None:

        _strings = OrderedDict()
        for i, string in enumerate(strings):
            _strings[string] = i
        self._strings = _strings

        self._setStringList(list(_strings.keys()))

    def appendString(self, qstr: str) -> None:

        if qstr not in self._strings:
            self._appendString(qstr)
        else:
            raise _UniqueStrError(qstr)


class ListView(QListView):

    def keyPressEvent(self, e):
        print(e)
        print(e.__class__)
