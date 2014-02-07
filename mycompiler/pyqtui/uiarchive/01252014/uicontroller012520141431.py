from mycompiler.pyqtui.base import UiControllerBase
from PyQt5.QtWidgets import QMainWindow


# noinspection PyMethodMayBeStatic
class UiController(UiControllerBase):
    ''' Controller for a PyQt5 uic-created ui, autogenerated
    from script pyqtui.uicompiler.py.
    
    Class body is generated from the list of connections
    found in the .ui file generated by QtDesigner, and should
    in all cases always have a list of every connection made
    with appropriate arguments, a simple docstring, and
    simple annotation.
    
    This class, located at:
    
    C:\Users\Administrator\Documents\Programming\PythonSource\source\mycompiler\pyqtui\uicontroller.py
    
    should therefore only be used with its co-generated class at:
    
    C:\Users\Administrator\Documents\Programming\PythonSource\source\mycompiler\pyqtui\ideui.py
    
    Failure to do so may result in mismatched signal/slot
    definitions in the view setupUi() protocol.
    
    '''

    def connectView(self, View):
        '''Connect the controller to an instance of a class
        corresponding to a PyQt5 uic-created UI.'''
        
        mainWindow = QMainWindow()
        View.setupUi(mainWindow, self)
        
        self.View = View
        self.mainWindow = mainWindow
        return None

    def changeCFlagMenuList(self, QString):
        '''
        @param QString:
        @type QString:
        @return:
        @rtype:
        '''
        print("changeCFlagMenuList called", QString)
        return None

    def cFlagListDoubleClick(self, QModelIndex):
        '''
        @param QModelIndex:
        @type QModelIndex:
        @return:
        @rtype:
        '''
        print("cFlagListDoubleClick called", QModelIndex)
        return None

    def cFlagAddClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("cFlagAddClicked called", QBool)
        return None

    def cFlagRemovedClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("cFlagRemovedClicked called", QBool)
        return None

    def cFlagCurrentDoubleClicked(self, QModelIndex):
        '''
        @param QModelIndex:
        @type QModelIndex:
        @return:
        @rtype:
        '''
        print("cFlagCurrentDoubleClicked called", QModelIndex)
        return None

    def outfileBrowseBtnClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("outfileBrowseBtnClicked called", QBool)
        return None

    def outfileEditReturnPressed(self, ):
        '''
        @param :
        @type :
        @return:
        @rtype:
        '''
        print("outfileEditReturnPressed called", )
        return None

    def compileClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("compileClicked called", QBool)
        return None

    def executeClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("executeClicked called", QBool)
        return None

    def runLastClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("runLastClicked called", QBool)
        return None

    def compilerChoiceMenuChanged(self, QString):
        '''
        @param QString:
        @type QString:
        @return:
        @rtype:
        '''
        print("compilerChoiceMenuChanged called", QString)
        return None

    def sourceBrowseBtnClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("sourceBrowseBtnClicked called", QBool)
        return None

    def generateMakefileClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("generateMakefileClicked called", QBool)
        return None

    def makefileSaveClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("makefileSaveClicked called", QBool)
        return None

    def makefileSaveAsClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("makefileSaveAsClicked called", QBool)
        return None

    def makefileOpenClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("makefileOpenClicked called", QBool)
        return None

    def runMakefileClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("runMakefileClicked called", QBool)
        return None

    def makefileDoUseClicked(self, QBool):
        '''
        @param QBool:
        @type QBool:
        @return:
        @rtype:
        '''
        print("makefileDoUseClicked called", QBool)
        return None

    def makefileDoActionChanged(self, QString):
        '''
        @param QString:
        @type QString:
        @return:
        @rtype:
        '''
        print("makefileDoActionChanged called", QString)
        return None
