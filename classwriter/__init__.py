__author__ = 'Nathan Starkweather'
'''

Created by: Nathan Starkweather
Created on: 01/20/2014
Created in: PyCharm Community Edition


'''

from classwriter.objproxies import ArgsProxy, FunctionProxy, ClassProxy, MethodProxy


# noinspection PyMethodMayBeStatic
class ClassWriter():
    """ This class should be written to be responsible for
    accepting some sort of contextual information from
    an outside source, and compiling a class body template
    according to that information.

    In all likelyhood, the context will simply be most convenient
    to implement as a dictionary, although an object (which
    in python is essentially just a fancy wrapper around a dictionary)
    may be more useful in the long run.

    To design the writer, consider the question of what,
    exactly, defines what a python class is? This class
    isn't intended to be a magical method-writer, but merely
    to handle the output of a valid set of contextual
    information into a form that is easily extensible by human
    readers.

    """

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

        save init args in case any context setup is required.
        """

        self.level = 0
        self.write_buffer = []

    def compileClass(self, klass: ClassProxy, outfile=None) -> None:
        """
        @param klass: classproxy to compile
        @type klass: ClassProxy
        @param outfile: file-like object (file, StringIO with a 'write' method)
        @type outfile: file-like object
        @return: None
        @rtype: None
        """
        # This seems a bit silly, but may be necessary later
        # if extra functionality required.

        decorators = self.build_class_decorators(klass)
        declaration = self.build_class_def(klass)
        ide_comments = self.build_ide_comments(klass)

        self.level += 1

        doc = self.build_class_doc(klass)
        klass_vars = self.build_class_vars(klass)

        bkm = self.build_class_method  # make next line shorter imsosorry
        klass_methods = [bkm(klass, mthdname, mthd) for mthdname, mthd in klass.methods.items()]

        write_code = self.write_code

        write_code(decorators)
        write_code(ide_comments)
        write_code(declaration)
        write_code(doc)  # probably several lines....
        write_code(klass_vars)

        for mthd in klass_methods:
            write_code(mthd)

        if outfile:
            self.Commit(outfile)

    def write_code(self, code: str):
        """
        @param code: line of code to write
        @type code: string
        @return: None
        @rtype: None

        If class needs to extended to maintain multiple buffers,
        write to a buffer stored in a dict keyed by klass's name.
        """

        self.write_buffer.append('\n' + code)

    def build_class_decorators(self, klass: ClassProxy) -> str:

        code = '\n'.join("@" + decorator for decorator in klass.decorators)
        return code

    def build_class_def(self, klass: ClassProxy) -> str:

        code = "class %s" % klass.name
        bases = klass.bases
        metaclass = klass.metaclass

        if bases and metaclass:
            obj_args = ', '.join(bases) + ', metaclass=' + metaclass
        elif bases:
            obj_args = ', '.join(bases)
        elif metaclass:
            obj_args = 'metaclass=' + metaclass
        else:
            obj_args = ''

        code += obj_args.join(('(', '):'))

        return code

    @property
    def spacer(self):
        return self.level * '    '

    def build_class_doc(self, klass: ClassProxy) -> str:
        """
        @param klass: ClassProxy
        @type klass: ClassProxy
        @return: docstring, indented to writer's current level
        @rtype: string

        Handle any special class-specific docstringing.
        """
        doc = klass.doc
        doc = self._build_proxy_doc(doc)

        return self._build_proxy_doc(doc)

    def _build_proxy_doc(self, doc: str) -> str:
        """Parse the klass doc and make sure that it
        gets indented correctly
        """
        doc = [line.strip() for line in doc.strip().split('\n')]
        doc[0] = self.spacer + doc[0]
        doc_str = ('\n' + self.spacer).join(doc)
        return doc_str

    def build_class_vars(self, klass: ClassProxy) -> str:
        var_string = '\n'.join("%s = %s" % (var, value) for var, value in klass.classvars)
        return var_string

    def build_class_method(self, klass: ClassProxy, methodname: str, method: FunctionProxy) -> str:
        return '\n'.join(self._build_class_method_list(klass, methodname, method))

    def _build_class_method_list(self, klass: ClassProxy, methodname: str, method: FunctionProxy) -> list:

        code = []  # list this time!

        for decorator in klass.decorators:
            code.append("@" + decorator)

        method_def = self.spacer + "def " + methodname
        arg_str = self.build_arg_string(method.args)

        method_def = ''.join((
                            method_def,
                            arg_str,
                            ':'
                            ))
        code.append(method_def)

        self.level += 1
        doc = self.build_function_doc(method)
        code.append(doc)

        body = self.build_function_body(method)
        code.append(body)
        code.append(self.spacer + 'return ' + (method.ret or 'None'))
        self.level -= 1
        code.append('')
        return code

    def build_arg_string(self, args: ArgsProxy) -> str:
        """
        @param args: Args instance with properly set values
        @type args: ArgsProxy
        @return: string of args in parenthesis as would be found in func def
        @rtype: str
        """

        pos_only_string = ', '.join(args.positional_only)
        pos_default_string = ', '.join("%s=%s" % (arg, val)
                                        for arg, val in args.positional_default.items())
        vararg_string = ("*" + args.varargs) if args.varargs else ''
        kwonly_string = ', '.join(args.kwonly)
        kwonly_default_string = ', '.join("%s=%s" % (arg, val)
                                          for arg, val in args.kwonly_default.items())
        varkwargs_string = ("**" + args.varkwargs) if args.varkwargs else ''

        # it takes a lot of if/else to determine when to place
        # a comma to separate elements of arg string,
        # so filter followed by ', '.join() does it for us.

        filtered_args = filter(None, (
                            pos_only_string,
                            pos_default_string,
                            vararg_string,
                            kwonly_string,
                            kwonly_default_string,
                            varkwargs_string
                            ))

        return '(' + ', '.join(filtered_args) + ')'

    def build_function_body(self, function: FunctionProxy) -> str:

        body = function.body
        if isinstance(body, str):
            body = (line.strip() for line in body.split('\n'))

        return self.spacer + ('\n' + self.spacer).join(body)

    def build_function_doc(self, func: FunctionProxy) -> str:
        """
        @param func: FunctionProxy
        @type func: FunctionProxy
        @return: docstring, indented to writer's current level
        @rtype: string

        Use for any special func-doc-related parsing
        """

        doc = func.doc
        if not doc:
            # if no docstring, make epydoc docstring
            doc = ["'''"]
            for arg in func.args:
                if arg != 'self':
                    doc.append("\n    @param %s:" % arg)
                    doc.append("\n    @type %s:" % arg)

            doc.append("\n    @return: ")
            doc.append("\n    @rtype: ")
            doc.append("\n    '''")

            doc = ''.join(doc)
        return self._build_proxy_doc(doc)

    def Commit(self, outfile):

        code = ''.join(self.write_buffer)

        # debug debug debug
        # print(code)
        # debug debug debug

        outfile.write(code)

    def reset(self):
        """
        @return: None
        @rtype: None
        Reset everything
        """

        self.write_buffer = []
        self.level = 0

    def build_ide_comments(self, proxy) -> str:
        return '\n'.join('# ' + comment for comment in proxy.ide_comments)


if __name__ == '__main__':
    c = ClassProxy(name='myklass')
    mthds = []
    for i in range(10):
        func = FunctionProxy(name='myfunc%d' % i)
        func.args.positional_only = ['fooarg', 'bararg']
        mthds.append(func)

    c.methods = mthds

    cw = ClassWriter()
    cw.compileClass(c)
