""" Base Module for active UiController.
"Active" meaning doing manual work on this file, as
opposed to the autogenerated file produced by uicompiler.py.

"""
from uibase import UiControllerBase
from ideui import IDEView
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QListView
from PyQt5.QtGui import QKeyEvent
import myqt
from weakref import ref


# noinspection PyMethodMayBeStatic
class UiController(UiControllerBase):
    """ Controller for a PyQt5 uic-created ui, autogenerated
    from script C:/Users/Administrator/Documents/Programming/PythonSource/source/mycompiler/pyqtui/uicompiler.py.

    Class body is generated from the list of connections
    found in the .ui file generated by QtDesigner, and should
    in all cases always have a list of every connection made
    with appropriate arguments, a simple docstring, and
    simple annotation.

    This class, located at:

    C:/Users/Administrator/Documents/Programming/PythonSource/source/mycompiler/pyqtui/uicontroller.py

    should therefore only be used with its co-generated class at:

    C:/Users/Administrator/Documents/Programming/PythonSource/source/mycompiler/pyqtui/ideui.py

    Failure to do so may result in mismatched signal/slot
    definitions in the view setupUi() protocol.

    """

    def __init__(self, app: QApplication):

        # Ui should only be imported once, so ok to leave
        # some imports here to avoid cluttering global namespace
        import config

        self._cfg_ops = config.cfg_ops
        self._cflags_ops = self._cfg_ops['cFlags']
        self._cflags_default = 'Warnings'

        # initialize vars
        self.View = None
        self.mainWindow = None
        self.cflagsListModel = None
        self.cflagsCategoryMenuModel = None
        self.cflagsActiveMenu = None
        self.cflagsCurrentListModel = None

        # weakref to app for app things
        self.QApp = app

    @property
    def QApp(self):
        return self._qApp()

    @QApp.setter
    def QApp(self, app: QApplication):
        self._qApp = ref(app)

    def connectView(self, View: IDEView):
        """
        @param View: compatible IDEView instance

        Connect the controller to an instance of a class
        corresponding to a PyQt5 uic-created UI.

        Special note: editing models here triggers signals to
        be received by slot functions, so assign model attrs
        to self as soon as they are defined, so that any
        self.model references in slots are valid.

        Note local references are used to make typing easier
        and cut down on doing eg self.View.Blah.Blah... all over
        """

        mainWindow = QMainWindow()
        self.mainWindow = mainWindow

        View.setupUi(mainWindow, self)
        self.View = View

        cflagsCategoryMenu = View.cflagsCategoryMenu
        cflagsList = View.cflagsList
        cflagsCurrentList = View.cflagsCurrentList

        cflagsList.setSelectionRectVisible(True)

        cflagsCurrentListModel = myqt.StringListModel(cflagsCurrentList)
        self.cflagsCurrentListModel = cflagsCurrentListModel

        cflagsCurrentList.setModel(cflagsCurrentListModel)

        cflagsCategoryMenuModel = cflagsCategoryMenu.model()
        self.cflagsCategoryMenuModel = cflagsCategoryMenuModel

        # Available Cflags
        cflagsListModel = myqt.StringListModel(cflagsList)
        self.cflagsListModel = cflagsListModel

        cflagsList.setModel(cflagsListModel)
        cflagsList.setEditTriggers(cflagsList.NoEditTriggers)

        # Initialize Available CFlags
        cflags_default_index = cflagsCategoryMenu.findText(self._cflags_default)
        cflagsCategoryMenu.setCurrentIndex(cflags_default_index)  # triggers changeCFlagMenuList(QStr)

        # Misc
        self._currentCflags = set()

        cflagsList.keyPressEvent = self.cflagsListKeyPressed

    def cflagsListKeyPressed(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.cFlagAddClicked(False)

    def changeCFlagMenuList(self, qstring: str) -> None:
        """
        @param qstring: name of the list to call
        @type qstring: string
        @return: None
        @rtype: None
        """

        if qstring != self.cflagsActiveMenu:
            self.cflagsListModel.setStringList(self._cflags_ops[qstring])
            self.cflagsActiveMenu = qstring

    def cFlagListDoubleClick(self, model_index: QModelIndex) -> None:
        """
        @param model_index: model index that was double clicked
        @type model_index: QModelIndex
        @return: None
        @rtype: None
        """

        self.appendCurrentCFlags(model_index.data())
        self.View.cflagsList.setFocus(True)

    # noinspection PyUnusedLocal
    def cFlagAddClicked(self, qbool: int) -> None:
        """
        @param qbool: dummy value, is always False
        @type qbool: Bool
        @return: None
        @rtype: None
        """

        flags = self.View.cflagsList
        index = flags.currentIndex()
        self.appendCurrentCFlags(index.data())
        flags.setFocus(True)

    # noinspection PyUnusedLocal
    def cFlagRemovedClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """

        flags = self.View.cflagsCurrentList
        modelIndex = flags.currentIndex()
        self.removeCurrentCFlag(modelIndex.data())
        flags.setFocus(True)

    def cFlagCurrentDoubleClicked(self, modelIndex: QModelIndex) -> None:
        """
        @param modelIndex:
        @type modelIndex:
        @return:
        @rtype:
        """

        self.removeCurrentCFlag(modelIndex.data())
        self.View.cflagsCurrentList.setFocus(True)

        return None

    def outfileBrowseBtnClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("outfileBrowseBtnClicked called", QBool)
        return None

    def outfileEditReturnPressed(self, ):
        """
        @param :
        @type :
        @return:
        @rtype:
        """
        print("outfileEditReturnPressed called", )
        return None

    def compileClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("compileClicked called", QBool)
        return None

    def executeClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("executeClicked called", QBool)
        return None

    def runLastClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("runLastClicked called", QBool)
        return None

    def compilerChoiceMenuChanged(self, qstring: str) -> None:
        """
        @param qstring:
        @type qstring:
        @return:
        @rtype:
        """
        print("compilerChoiceMenuChanged called", qstring)
        return None

    def sourceBrowseBtnClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("sourceBrowseBtnClicked called", QBool)
        return None

    def generateMakefileClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("generateMakefileClicked called", QBool)
        return None

    def makefileSaveClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("makefileSaveClicked called", QBool)
        return None

    def makefileSaveAsClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("makefileSaveAsClicked called", QBool)
        return None

    def makefileOpenClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("makefileOpenClicked called", QBool)
        return None

    def runMakefileClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("runMakefileClicked called", QBool)
        return None

    def makefileDoUseClicked(self, QBool: int) -> None:
        """
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        """
        print("makefileDoUseClicked called", QBool)
        return None

    def makefileDoActionChanged(self, qstring: str) -> None:
        """
        @param qstring:
        @type qstring:
        @return:
        @rtype:
        """
        print("makefileDoActionChanged called", qstring)
        return None

    def appendCurrentCFlags(self, flag: str) -> None:
        """
        @param flag: str of flag pending addition
        @type flag: str
        @return: None
        @rtype: None
        """

        if flag and flag not in self._currentCflags:
            self.cflagsCurrentListModel.appendString(flag)
            self._currentCflags.add(flag)
        else:
            self.QApp.beep()

    def isNewCurrentCFlag(self, flag: str) -> int:
        """
        @param flag: flag to check for presence in current cflags list
        """
        return bool(flag) and flag not in self._currentCflags

    def removeCurrentCFlag(self, flag: str) -> None:
        """
        @param flag: flag to remove from current list
        @type flag: str
        @return: None
        @rtype: None
        """

        if flag and flag in self._currentCflags:
            self.cflagsCurrentListModel.removeString(flag)
            self._currentCflags.remove(flag)
        else:
            self.QApp.beep()
if __name__ == "__main__":

    from sys import argv

    def testui():
        """
        @return: None
        @rtype: None
        """
        app = QApplication(argv)
        c = UiController(app)
        v = IDEView()

        c.connectView(v)
        c.mainWindow.show()

        app.exec()

    testui()
