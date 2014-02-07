

class UiController(UiControllerBase):
    ''' Controller for a PyQt5 uic-created ui, autogenerated
    from script pyqtui.uicompiler.py.
    
    Class body is generated from the list of connections
    found in the .ui file generated by QtDesigner, and should
    in all cases always have a list of every connection made
    with appropriate arguments, a simple docstring, and
    simple annotation.
    
    This class, located at:
    
    C:\Users\Administrator\Documents\Programming\PythonSource\source\mycompiler\pyqtui\ideui_debug.py
    
    should therefore only be used with its co-generated class at:
    
    C:\Users\Administrator\Documents\Programming\PythonSource\source\mycompiler\pyqtui\uicontroller_debug.py
    
    Failure to do so may result in mismatched signal/slot
    definitions in the view setupUi() protocol.
    
    '''

    def changeCFlagMenuList(self, QString):
        '''Signal handler from widget 'cflagsCategoryMenu' connecting
        signal'QString'.
        '''
        print("changeCFlagMenuList called", QString)

    def cFlagListDoubleClick(self, QModelIndex):
        '''Signal handler from widget 'cflagsList' connecting
        signal'QModelIndex'.
        '''
        print("cFlagListDoubleClick called", QModelIndex)

    def cFlagAddClicked(self, QBool):
        '''Signal handler from widget 'cflagsAddBtn' connecting
        signal'QBool'.
        '''
        print("cFlagAddClicked called", QBool)

    def cFlagRemovedClicked(self, QBool):
        '''Signal handler from widget 'cflagsRemoveBtn' connecting
        signal'QBool'.
        '''
        print("cFlagRemovedClicked called", QBool)

    def cFlagCurrentDoubleClicked(self, QModelIndex):
        '''Signal handler from widget 'cflagsCurrentList' connecting
        signal'QModelIndex'.
        '''
        print("cFlagCurrentDoubleClicked called", QModelIndex)

    def outfileBrowseBtnClicked(self, QBool):
        '''Signal handler from widget 'browseOutfileBtn' connecting
        signal'QBool'.
        '''
        print("outfileBrowseBtnClicked called", QBool)

    def outfileEditReturnPressed(self, ):
        '''Signal handler from widget 'browseOutfileEdit' connecting
        signal''.
        '''
        print("outfileEditReturnPressed called", )

    def compileClicked(self, QBool):
        '''Signal handler from widget 'compileBtn' connecting
        signal'QBool'.
        '''
        print("compileClicked called", QBool)

    def executeClicked(self, QBool):
        '''Signal handler from widget 'executeBtn' connecting
        signal'QBool'.
        '''
        print("executeClicked called", QBool)

    def runLastClicked(self, QBool):
        '''Signal handler from widget 'runLastBtn' connecting
        signal'QBool'.
        '''
        print("runLastClicked called", QBool)

    def compilerChoiceMenuChanged(self, QString):
        '''Signal handler from widget 'ccChoiceMenu' connecting
        signal'QString'.
        '''
        print("compilerChoiceMenuChanged called", QString)

    def sourceBrowseBtnClicked(self, QBool):
        '''Signal handler from widget 'browseSourceBtn' connecting
        signal'QBool'.
        '''
        print("sourceBrowseBtnClicked called", QBool)

    def generateMakefileClicked(self, QBool):
        '''Signal handler from widget 'generateMakefileBtn' connecting
        signal'QBool'.
        '''
        print("generateMakefileClicked called", QBool)

    def makefileSaveClicked(self, QBool):
        '''Signal handler from widget 'makefileSaveBtn' connecting
        signal'QBool'.
        '''
        print("makefileSaveClicked called", QBool)

    def makefileSaveAsClicked(self, QBool):
        '''Signal handler from widget 'makefileSaveAsBtn' connecting
        signal'QBool'.
        '''
        print("makefileSaveAsClicked called", QBool)

    def makefileOpenClicked(self, QBool):
        '''Signal handler from widget 'makefileOpenBtn' connecting
        signal'QBool'.
        '''
        print("makefileOpenClicked called", QBool)

    def runMakefileClicked(self, QBool):
        '''Signal handler from widget 'makefileRunBtn' connecting
        signal'QBool'.
        '''
        print("runMakefileClicked called", QBool)

    def makefileDoUseClicked(self, QBool):
        '''Signal handler from widget 'makefileCkBox' connecting
        signal'QBool'.
        '''
        print("makefileDoUseClicked called", QBool)

    def makefileDoActionChanged(self, QString):
        '''Signal handler from widget 'makefileRunMenu' connecting
        signal'QString'.
        '''
        print("makefileDoActionChanged called", QString)
