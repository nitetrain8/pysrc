__author__ = 'Nathan Starkweather'
'''

Created by: Nathan Starkweather
Created on: 01/25/2014
Created in: PyCharm Community Edition


'''

from ideui import IDEView
from uicontroller import UiController
from PyQt5.QtWidgets import QApplication
from sys import argv


def ShowUi():
    app = QApplication(argv)
    c = UiController()
    v = IDEView()

    c.connectView(v)
    c.mainWindow.show()

    app.exec()


if __name__ == '__main__':
    ShowUi()

