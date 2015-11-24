__author__ = 'Administrator'
'''Created on 1/16/14'''

from datetime import datetime
from os import makedirs

from PyQt5.uic.Compiler.indenter import getIndenter, write_code
from PyQt5.uic.Compiler import qtproxies

from guicompiler.guicompilerbase import _GuiCompiler


uifile = 'C:\\Python33\\Lib\\site-packages\\PyQt5\\myprojects\\ui\\MyIDE.ui'
pyqtui_folder = 'C:\\Users\\Administrator\\Documents\\Programming\\PythonSource\\source\\mycompiler\\pyqtui'
view_file = 'ideui.py'
controller_file = 'uicontroller.py'

view_file_backup = 'ideui%m%d%Y%H%M.py'
backup_folder = 'C:\\Users\\Administrator\\Documents\\Programming\\PythonSource\\source\\mycompiler\\pyqtui\\uiarchive\\%m%d%Y'
controller_file_backup = "uicontroller%m%d%Y%H%M.py"


class PyQtGuiCompiler(_GuiCompiler):
    """The main class to use to hook into the UIC api.

    Inherit _GuiCompiler for debugging purposes, eventually should
    just inherit UIcompiler directly with no special metaclass.

    Class for writing files related to ui
    compilation.

    This class currently doesn't have any options
    to customize the input or output file beyond
    changing the paths at the top of the module.

    This is written to be a one-off easy access
    to press a button fire-and-forget to creating
    Ui files.

    Update 1/18/2014:

    Now PyQtGuiCompiler and UiWriter merged into one
    class. It only made sense before to have them
    separate due to legacy development during proof-
    of-concept stage.

    Update 1/19/2014:

    It might be slightly odd to both intercept UIC
    and create our own writer in the same class,
    but the functionality is currently intimately
    tied. Perhaps it would be smarter instead to
    hook createConnections() by creating a list of
    signals and slots, and exporting it to a class
    variable which can be easily retrieved.

    Actually, that's exactly what should have been done.
    The controller creation is somewhat distinct from the UI
    creation; the only relationship they have is in signals
    and slots.

    Todo- that.

    """

    ui_cls_name = "%sView"
    ui_cls_name_def = "class %s():" % ui_cls_name
    setup_ui_def = "def setupUi(self, %s, controller):"

    view_import_def = "from PyQt5 import QtWidgets, QtCore"

    controller_imports = [
                          "from mycompiler.pyqtui.base import UiControllerBase",
                          "from PyQt5.QtWidgets import QMainWindow"
                         ]
    controller_cls_def = "class UiController(UiControllerBase):"
    controller_doc = '''
    \'\'\' Controller for a PyQt5 uic-created ui, autogenerated
    from script pyqtui.uicompiler.py.

    Class body is generated from the list of connections
    found in the .ui file generated by QtDesigner, and should
    in all cases always have a list of every connection made
    with appropriate arguments, a simple docstring, and
    simple annotation.

    This class, located at:

    %s

    should therefore only be used with its co-generated class at:

    %s

    Failure to do so may result in mismatched signal/slot
    definitions in the view setupUi() protocol.

    \'\'\'''' % ('\\'.join((pyqtui_folder, controller_file)).replace('\\', '\\\\'),
                 '\\'.join((pyqtui_folder, view_file)).replace('\\', '\\\\'))

    controller_init = '''def __init__(self):
        \'\'\' Placeholder \'\'\'
        pass
        '''
    controller_connectview = '''def connectView(self, View: object):
        \'\'\'Connect the controller to an instance of a class
         corresponding to a PyQt5 uic-created UI.

        \'\'\'
        mainWindow = QMainWindow()
        View.setupUi(mainWindow, self)

        self.View = View
        self.mainWindow = mainWindow'''
    controller_connect_body = 'self.mainWindow = QMainWindow()'
    # controller_init_body = ['self.view = view', 'self.mainWindow = mainWindowWidget']
    controller_slot_body = 'pass'
    controller_slot_def = "def %s(self%s):"

    import atexit

    register = atexit.register
    unregister = atexit.unregister

    def __init__(self):

        """Initialize writer with module level settings.
        The module settings and writer logic take care of
        everything. Fire and forget.

        Target_folder - the save target folder

        controller_file - the target filename including
        extension. Because the target folder may need
        to be created, we keep track of them separately
        and join them together when we're ready to
        commit the write.
        """

        self.uifile = uifile
        self.view_file = view_file
        self.controller_file = controller_file
        self.target_folder = pyqtui_folder

        self.view_file_backup = view_file_backup
        self.backup_folder = backup_folder
        self.controller_file_backup = controller_file_backup

        self.written_files = []

        self.level = 0
        self._write_buffer = []
        self.register(self.Commit)

        super().__init__()

    def _createConnections(self, elem):
        """This is the big important function. This can
        be used with the hookConnections() (or just removing the '_')
        to hook into the signal/slot creation logic from UICompiler.

        This lets us redirect and customize how we want to do the creation.

        1/18/2014- Currently function is a bit of a mess since it is all
         in debug mode.
        """

        write = self.write
        write_list = self.write_list
        indent = self.indent
        dedent = self.dedent

        # wrap the passed thing in quotes.
        quotify = lambda x: ''.join(('\'', x, '\''))

        py_uic_write = write_code  # imported from pyqt5 indenter module

        write("")
        write_list(self.controller_imports)
        write("")

        write("# noinspection PyMethodMayBeStatic")
        write(self.controller_cls_def)

        indent()
        write(self.controller_doc)
        write("")

        write(self.controller_init)

        write(self.controller_connectview)

        slots = []
        senders = []
        args = []
        connections_list = []

        for conn in elem:
            sender = conn.findtext('sender')
            signal = conn.findtext('signal')
            slot = conn.findtext('slot')

            slot_name, _slot_args = slot.split('(')
            sig, sig_args = signal.split('(')
            sig_args = sig_args[:-1].replace(' ', '')

            if sig_args:
                sig_connection_type = "%s['%s']" % (sig, sig_args)
            else:
                sig_connection_type = sig

            connect_code = ("self.%s.%s.connect(controller.%s)" % (sender,
                                                                   sig_connection_type,
                                                                   slot_name))
            py_uic_write(connect_code)

            controller_slot_doc = [
                                    '\'\'\'Signal handler from widget \'%s\'' % sender,
                                    'connecting signal \'%s\'.' % sig_connection_type,
                                    '',
                                    '\'\'\''
                                    ]

            slot_arg_def = (', signal: \'%s\'' % sig_args) if sig_args else ''

            write("")
            write(self.controller_slot_def % (slot_name, slot_arg_def))

            indent()

            write_list(controller_slot_doc)
            if sig_args:
                write("print(signal)")
            else:
                write("pass")

            dedent()

            slots.append(quotify(slot_name))
            senders.append(quotify(sender))
            args.append(quotify(sig_args))
            connections_list.append((slot_name, sig_args, sender))

        write('')
        # self.make_code_list('slots', slots)
        # self.make_code_list('senders', senders)
        # self.make_code_list('signals', args)

        self.connections_list = connections_list

        write("# End Connections")

    def finalize(self):
        """Mostly copy/paste from compiler.py, but I need to
        make a change in the middle of the code to stick a #ignoreanalysis
        tag in, so no super() call.

        """
        indenter = getIndenter()
        indenter.level = 1
        indenter.write("")
        indenter.write("# noinspection PyTypeChecker")
        indenter.write("def retranslateUi(self, %s):" % self.toplevelWidget)

        indenter.indent()

        if qtproxies.i18n_strings:
            indenter.write("_translate = QtCore.QCoreApplication.translate")
            for s in qtproxies.i18n_strings:
                indenter.write(s)
        else:
            indenter.write("pass")

        indenter.dedent()
        indenter.dedent()

        # Make a copy of the resource modules to import because the parser will
        # _internal_reset() before returning.
        self._resources = self.resources

    # hook/unhook UICompiler's createConnections
    # first sets class variable to default
    # second saves a hard reference to swap at will
    createConnections = _GuiCompiler.createConnections
    super_createConnections = createConnections

    def hookConnections(self):
        self.createConnections = self._createConnections

    def unhookConnections(self):
        self.createConnections = self.super_createConnections

    @property
    def indenter(self) -> "PyQt5 _IndentedCodeWriter":
        """Simple property to ensure that compiler class
        always has access to the PyUIC indenter via the
        proper channel.
        """
        return getIndenter()

    def createToplevelWidget(self, classname, widgetname):
        """This is mostly copy/pasted from the UIC code,
        but with some small changes that allow some
        custom creation of the class name and setupUi
        code.
        """

        indenter = getIndenter()
        indenter.level = 0

        indenter.write(self.view_import_def)
        indenter.write("")

        indenter.write(self.ui_cls_name_def % "IDE")
        indenter.indent()
        indenter.write(self.setup_ui_def % widgetname)
        indenter.indent()
        w = self.factory.createQObject(classname, widgetname, (),
                                       is_attribute=False,
                                       no_instantiation=True)
        w.baseclass = classname
        w.uiclass = self.ui_cls_name % self.uiname
        return w

    def createModule(self):

        with open(self.uifile, 'r') as uifile:
            with open(self.view_file, 'w') as pyfile:
                self.compileUi(input_stream=uifile,
                               output_stream=pyfile,
                               from_imports=False,
                               resource_suffix='_rc')

    def indent(self, n: int=1):
        self.level += n

    def dedent(self, n: int=1):
        self.level -= n
        if self.level < 0:
            raise ValueError("Internal Error: dedented below 0")

    def getLast(self) -> str:
        """Get last action written to write buffer
        If the last action was a write_list, returns whole
        list.
        """

        return self._write_buffer[-1]

    def Undo(self) -> str:
        """Undo last write. If the last write was a list,
        undo the whole list.

        Return the value just in case user wanted to work
        with it.
        """

        return self._write_buffer.pop()

    @property
    def spacer(self):
        return self.level * '    '

    def write_list(self, code_list: list):
        """Write a list of strings instead of just a string.
        Convert to a joined string and send to self.write.

        This way all writing to the write buffer can be done
        through a single function, to ensure that any shenanigans
        that may be necessary can be performed there.

        the [self.level * 4:-1] strips off redundant whitespace
        added when the string is passed to self.write
        """

        self.write(''.join(''.join((self.spacer, code, '\n')) for code in code_list)[self.level * 4:])

    def write(self, code: str):
        self._write_buffer.append(''.join((self.spacer, code, '\n')))

    # noinspection PyMethodMayBeStatic
    def FormatArchiveName(self, folder: str, filename: str) -> str:
        """ Handle the formatting of filename templates
        using strftime.

        Generally, call datetime.now(), and run strftime
        on the passed templates, and return a
        3- tuple of folder, filename, and full filepath (joined).

        Pass in the strftime-compatible folder and filenames, get a
        3-tuple back

        """

        now = datetime.now()
        filename = now.strftime(filename)
        folder = now.strftime(folder)
        filepath = '\\'.join((folder, filename))

        try:
            makedirs(folder)
        except OSError:  # folder already existed
            pass

        return filepath

    def _write_commit(self):
        """Warning! This opens the file for writing, overriding
        all contents inside! Don't call until ready! Also creates backups
        of both controller and view file. The most recently created file goes
        in the main folder, backups also written to archive.


        """

        cntrlr_bkup = self.FormatArchiveName(self.backup_folder, self.controller_file_backup)
        code = ''.join(self._write_buffer)

        with open(self.controller_file, 'w') as f:
            f.write(code)

        # Create backup

        with open(cntrlr_bkup, 'w') as f:
            f.write(code)

        self.written_files.append(cntrlr_bkup)
        self._write_buffer = []

    def _backup_view(self):
        """Create a backup of the most recent viewfile.

        Make separate function to allow explicit calling.

        """

        view_path = '\\'.join((self.target_folder, self.view_file))

        with open(view_path, 'r') as f:
            view_code = f.read()

        view_bkup = self.FormatArchiveName(self.backup_folder, self.view_file_backup)

        with open(view_bkup, 'w') as f:
            f.write(view_code)

        self.written_files.append(view_bkup)

    def _write_console(self):
        """Identical to above, except write to console
        instead of writing to file.

        Primary use for debugging.
        """

        cntrlr_bkup = self.FormatArchiveName(self.backup_folder, self.controller_file_backup)

        print(cntrlr_bkup)
        print(''.join(self._write_buffer))

        self._write_buffer = []

    def make_code_list(self, varname: str, item_list: list, write_list=write_list, write=write):
        """Write out a literal list of items in the code.
        ie, mylist = [1,2,3]. Helper function since the code sequence
        is ugly. Feed in the item list as a list of strings if
        you want the list to be a list of strings instead of items.
        """

        write(self, "%s = [" % varname)
        self.indent(2)
        list_code = ["%s," % item for item in item_list]
        list_code.append(']')
        write_list(self, list_code)
        self.dedent(2)

    def Commit(self):
        """call _write_commit. For now that's all it needs to do
        may need to do more later.

        This function is registered to run at exit during __init__,
        so unregister it manually if called before then.
        """

        # self._write_console()  # DEBUG setting
        self._write_commit()  # Normal setting
        self._backup_view()

        try:
            self.unregister(self.Commit)
        except:
            pass

        print("Success! Following files written:")
        for file in self.written_files:
            print("  ", file)

        self._write_buffer = None  # Don't allow any additions.


def main():
    c = PyQtGuiCompiler()
    c.hookConnections()
    c.createModule()
    c.Commit()


if __name__ == '__main__':
    main()
