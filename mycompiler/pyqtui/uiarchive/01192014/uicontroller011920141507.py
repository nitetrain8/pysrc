
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

    C:\\Users\\Administrator\\Documents\\Programming\\PythonSource\\source\\mycompiler\\pyqtui\\uicontroller.py

    should therefore only be used with its co-generated class at:

    C:\\Users\\Administrator\\Documents\\Programming\\PythonSource\\source\\mycompiler\\pyqtui\\ideui.py.

    Failure to do so may result in mismatched signal/slot
    definitions in the view setupUi() protocol.

    '''
    
    def __init__(self):
        ''' Placeholder '''
        pass
        
    def connectView(self, View: object):
        '''Connect the controller to an instance of a class
         corresponding to a PyQt5 uic-created UI.

        '''
        mainWindow = QMainWindow()
        View.setupUi(mainWindow, self)

        self.View = View
        self.mainWindow = mainWindow
    
    def changeCFlagMenuList(self, signal: 'QString'):
        '''Signal handler from widget 'cflagsCategoryMenu'
        connecting signal 'currentIndexChanged['QString']'.
        
        '''

        print(signal)
    
    def cFlagListDoubleClick(self, signal: 'QModelIndex'):
        '''Signal handler from widget 'cflagsList'
        connecting signal 'doubleClicked['QModelIndex']'.
        
        '''

        print(signal)
    
    def cFlagAddClicked(self):
        '''Signal handler from widget 'cflagsAddBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def cFlagRemovedClicked(self):
        '''Signal handler from widget 'cflagsRemoveBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def cFlagCurrentDoubleClicked(self, signal: 'QModelIndex'):
        '''Signal handler from widget 'cflagsCurrentList'
        connecting signal 'doubleClicked['QModelIndex']'.
        
        '''

        print(signal)
    
    def outfileBrowseBtnClicked(self):
        '''Signal handler from widget 'browseOutfileBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def outfileEditReturnPressed(self):
        '''Signal handler from widget 'browseOutfileEdit'
        connecting signal 'returnPressed'.
        
        '''

        pass
    
    def compileClicked(self):
        '''Signal handler from widget 'compileBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def executeClicked(self):
        '''Signal handler from widget 'executeBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def runLastClicked(self):
        '''Signal handler from widget 'runLastBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def compilerChoiceMenuChanged(self, signal: 'QString'):
        '''Signal handler from widget 'ccChoiceMenu'
        connecting signal 'currentIndexChanged['QString']'.
        
        '''

        print(signal)
    
    def sourceBrowseBtnClicked(self):
        '''Signal handler from widget 'browseSourceBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def generateMakefileClicked(self):
        '''Signal handler from widget 'generateMakefileBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def makefileSaveClicked(self):
        '''Signal handler from widget 'makefileSaveBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def makefileSaveAsClicked(self):
        '''Signal handler from widget 'makefileSaveAsBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def makefileOpenClicked(self):
        '''Signal handler from widget 'makefileOpenBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def runMakefileClicked(self):
        '''Signal handler from widget 'makefileRunBtn'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def makefileDoUseClicked(self):
        '''Signal handler from widget 'makefileCkBox'
        connecting signal 'clicked'.
        
        '''

        pass
    
    def makefileDoActionChanged(self, signal: 'QString'):
        '''Signal handler from widget 'makefileRunMenu'
        connecting signal 'currentTextChanged['QString']'.
        
        '''

        print(signal)
    
    # End Connections
