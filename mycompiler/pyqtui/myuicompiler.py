
from PyQt5.uic.Compiler.indenter import write_code as indenter_write_code, getIndenter
from mycompiler.pyqtui.base import MyUiBase, UiControllerBase

uifile = 'C:\\Python33\\Lib\\site-packages\\PyQt5\\myprojects\\ui\\MyIDE.ui'
outfile = 'C:\\Users\\Administrator\\Documents\\Programming\\PythonSource\\source\\mycompiler\\pyqtui\\ideui.py'
modelfile = 'C:\\Users\\Administrator\\Documents\\Programming\\PythonSource\\source\\mycompiler\\pyqtui\\uimodel.py'
  
  
class MyIndenter():
    
    import atexit
    register = atexit.register
    unregister = atexit.unregister
    
    def __init__(self, outfile: str):

        self.file = None
        self.filename = outfile
        f = open(self.filename, 'w')
        f.close()  # truncate
            
        self.register(self.flush)

        self.level = 0
        self._write_buffer = []
        global myindenter
        myindenter = self
        
    def indent(self):
        self.level += 1
    
    def dedent(self):
        self.level -= 1

    def setFile(self, outfile: str):
        self.filename = outfile

    @property
    def spacer(self):
        return self.level * 4 * ' '
    
    def write(self, code):

        if isinstance(code, list):
            out = ''.join([''.join((self.spacer, c, '\n')) for c in code])
        else:
            out = ''.join((self.spacer, code, '\n'))
        self._write(out)
        
    def _push_buffer(self, code):
        self._write_buffer.append(code)
        
    def _do_write(self, code):
        
        if not self.file:
            self.openFile()

        if self._write_buffer:
            buf_code = ''.join(self._write_buffer)
        else:
            buf_code = ''

        self.file.write('\n'.join((buf_code, code)))

    _write = _push_buffer
    
    def openFile(self):
        self.file = open(self.filename, 'a')
        self.register(self.closeFile)
    
    def flush(self):
        print("flushing!")
        if self._write_buffer:
            self._do_write(''.join(self._write_buffer))
        self._write_buffer = []

    # noinspection PyUnusedLocal
    def __del__(self, *args):
        ''' Ensure buffer is flushed when closing!
        __del__ is unreliable but better than nothing.
        Better to call Finish() explicitly.

        @param args: the args normally sent to del.

        '''
        if self._write_buffer:
            print("You fool! Flush files before closing!")
        self._cleanup()
        print("deleting self, closing file!")
        
    def _cleanup(self):

        self.unregister(self.flush)
        self.unregister(self.closeFile)
        self.flush()
        self.closeFile()

    def closeFile(self):
        try:
            self.file.close()
        except (IOError, OSError):
            raise
        except:
            pass
        self.unregister(self.closeFile)

    def finish(self):
        try:
            self._cleanup()
        except:
            pass
    
myindenter = None


def getMyIndenter():
    global myindenter
    if myindenter is None:
        myindenter = MyIndenter(modelfile)
    return myindenter


def makeIndenter(outfile):
    global myindenter
    del myindenter
    myindenter = MyIndenter(outfile)


def write_code(code):
    
    getMyIndenter().write(code)
    

class MyUiCompiler(MyUiBase):
    
    '''PyQt's UIC module is beautifully written, but
    contains some minor issues that I would consider to be
    not quite flaws, but slight oversights. 
    
    In particular, excessive use of magic strings and numbers 
    throughout the UICompiler class, which makes it difficult 
    to subclass, because I have to copy/paste the superclass 
    implementation of some functions just to change a single 
    line of output.
    
    Since I don't know wtf I'm doing, I've moved some magic strings
    and other class variables up here, to make it easier to edit and 
    subclass
    '''

    ui_cls_name = "%sView"
    ui_cls_name_def = "class %s():" % ui_cls_name
    setup_ui_def = "def setupUi(self, %s, abstractModel):"
    import_def = "from PyQt5 import QtCore, QtGui, QtWidgets"
    model_cls_def = "class UiController(UiControllerBase):"
    model_init_def = '''def __init__(self, mainWindowWidget, view):'''
    model_init_body = ['self.view = view', 'self.mainWindow = mainWindowWidget']
    model_slot_body = 'pass'
    model_slot_def = "def %s(self%s):\n"
     
    def __init__(self, uifile=None, viewfile=None, modelfile=None):
        
        self.uifile = uifile
        self.viewfile = viewfile
        self.modelfile = modelfile

        self.indenter = MyIndenter(modelfile) if modelfile else None

        super().__init__()
    
    def _createConnections(self, elem):
        
        # vwrite_code = self.write_code
        indenter = self.indenter

        write = indenter.write
    
        write(self.model_cls_def)
        indenter.indent()

        write(self.model_init_def)
        indenter.indent()
        assert isinstance(self.model_init_body, list)
        write(self.model_init_body)
        indenter.dedent()
    
        for conn in elem:
            sender = conn.findtext('sender')
            receiver = conn.findtext('receiver')
            signal = conn.findtext('signal')
            slot = conn.findtext('slot')
   
            slot_name, slot_args = slot.split('(')
            sig, sig_args = signal.split('(')
            sig_args = sig_args[:-1].replace(' ', '')
   
            # sig_argstr = "%s['%s']" % (sig, sig_args) if sig_args else sig
            # code = ("self.%s.%s.connect(self.%s)" % (sender,
            #                                          sig_argstr,
            #                                          slot.split('(')[0]))

            sig_args = (', ' + sig_args) if sig_args else ''

            write("")
            write(self.model_slot_def % (slot_name, sig_args))
            indenter.indent()
            # vwrite_code("debug was here: %s %s %s %s" % (sender, signal, receiver, slot))
            write("\'\'\'debug was here:\'\'\' \n        \'\'\'%s %s %s %s\'\'\'" % (sender, signal, receiver, slot))

#             write(self.model_slot_body)
            write("print('%s called!')" % slot)
            indenter.dedent()
        write("\'\'\'End Connections\'\'\'")

    # hook/unhook UICompiler's createConnections
    createConnections = MyUiBase.createConnections
    super_createConnections = createConnections    

    def hookConnections(self):
        self.createConnections = self._createConnections
        
    def unhookConnections(self):
        self.createConnections = self.super_createConnections
        
    def createModule(self, uifile=None, viewfile=None, modelfile=None):
        
        uifile = uifile or self.uifile
        viewfile = viewfile or self.viewfile
        modelfile = modelfile or self.modelfile
        
        ui = open(uifile, 'r')
        pyfile = open(viewfile, 'w')
        if self.indenter is None:
            self.indenter = MyIndenter(modelfile)

        self.compileUi(input_stream=ui,
                       output_stream=pyfile,
                       from_imports=False,
                       resource_suffix='_rc'
                       )

        ui.close()
        pyfile.close()

    @staticmethod
    def write_code(code, out_func=indenter_write_code):
        out_func(code)
        
    def finalize(self):
        self.indenter.flush()
        super().finalize()

    def createToplevelWidget(self, classname, widgetname):
        
        indenter = getIndenter()
        indenter.level = 0

        indenter.write(self.import_def)
        indenter.write("")

        indenter.write(self.ui_cls_name_def % self.uiname)
        indenter.indent()
        indenter.write(self.setup_ui_def % widgetname)
        indenter.indent()
        w = self.factory.createQObject(classname, widgetname, (),
                                       is_attribute=False,
                                       no_instantiation=True)
        w.baseclass = classname
        w.uiclass = self.ui_cls_name % self.uiname
        return w

              
if __name__ == '__main__':
    
    m = MyUiCompiler(uifile, outfile, modelfile)
    m.hookConnections()
    m.createModule()
    getMyIndenter().finish()
    
    mydict = {'UiControllerBase' : UiControllerBase}
    with open(modelfile, 'r') as f:
        exec(f.read(), mydict)
    for k, v in mydict.items():
        print(k, v)   
    
