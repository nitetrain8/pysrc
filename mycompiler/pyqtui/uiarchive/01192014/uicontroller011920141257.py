
from mycompiler.pyqtui.base import UiControllerBase


# noinspection PyMethodMayBeStatic
class UiController(UiControllerBase):
    def __init__(self):
        pass
    
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
    
    slots = [
            'changeCFlagMenuList',
            'cFlagListDoubleClick',
            'cFlagAddClicked',
            'cFlagRemovedClicked',
            'cFlagCurrentDoubleClicked',
            'outfileBrowseBtnClicked',
            'outfileEditReturnPressed',
            'compileClicked',
            'executeClicked',
            'runLastClicked',
            'compilerChoiceMenuChanged',
            'sourceBrowseBtnClicked',
            'generateMakefileClicked',
            'makefileSaveClicked',
            'makefileSaveAsClicked',
            'makefileOpenClicked',
            'runMakefileClicked',
            'makefileDoUseClicked',
            'makefileDoActionChanged',
            ]

    senders = [
            'cflagsCategoryMenu',
            'cflagsList',
            'cflagsAddBtn',
            'cflagsRemoveBtn',
            'cflagsCurrentList',
            'browseOutfileBtn',
            'browseOutfileEdit',
            'compileBtn',
            'executeBtn',
            'runLastBtn',
            'ccChoiceMenu',
            'browseSourceBtn',
            'generateMakefileBtn',
            'makefileSaveBtn',
            'makefileSaveAsBtn',
            'makefileOpenBtn',
            'makefileRunBtn',
            'makefileCkBox',
            'makefileRunMenu',
            ]

    signals = [
            'cflagsCategoryMenu',
            'cflagsList',
            'cflagsCurrentList',
            'ccChoiceMenu',
            'makefileRunMenu',
            ]

    # End Connections
