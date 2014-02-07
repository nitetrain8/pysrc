__author__ = 'Nathan Starkweather'
'''

Created by: Nathan Starkweather
Created on: 01/19/2014
Created in: PyCharm Community Edition


'''

from uicontroller import UiController
from ideui import IDEView

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import QModelIndex, QVariant
from PyQt5.Qt import *

from sys import argv

app = QtWidgets.QApplication(argv)
c = UiController()
v = IDEView()

c.connectView(v)

# model = QStandardItemModel()
# c.View.cflagsList.setModel(model)
#
# for i in range(5):
#     myitem = QStandardItem("foo%d" % i)
#     myitem2 = QStandardItem("foo2.%d" % i)
#     model.appendRow(myitem)

c.mainWindow.show()

app.exec()
