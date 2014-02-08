__author__ = 'Nathan Starkweather'
'''

Created by: Nathan Starkweather
Created on: 02/06/2014
Created in: PyCharm Community Edition


'''
from PyQt5.QtCore import QStringListModel

class StringListModel(QStringListModel):
    def append(self, qstr: str) -> None:
        row = self.rowCount()
        self.insertRows(row, 1)
        index = self.index(row)
        self.setData(index, qstr)



