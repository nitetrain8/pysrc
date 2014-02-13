__author__ = 'Nathan Starkweather'
'''

Created by: Nathan Starkweather
Created on: 01/25/2014
Created in: PyCharm Community Edition


'''


class ProxyError(Exception):
    pass


class ArgsProxy():
    """Helper class to make working with
    args for FunctionProxy easier.
    """
    __slots__ = [
        'positional_only',
        'positional_default',
        'varargs',
        'kwonly',
        'kwonly_default',
        'varkwargs'
    ]

    def __init__(self,
                 positional_only: list=None,
                 positional_default: dict=None,
                 varargs: str='',
                 kwonly: list=None,
                 kwonly_default: dict=None,
                 varkwargs: str=''):
        """
        @param positional_only: list of positional only args
        @type positional_only: list
        @param positional_default: mapping of names to default values
        @type positional_default: dict
        @param varargs: string to use for * variable
        @type varargs: str
        @param kwonly: list of args that are kwonly
        @type kwonly: list
        @param kwonly_default: mapping of kwonly names to default values
        @type kwonly_default: dict
        @param varkwargs: string for ** variable
        @type varkwargs: str
        @return: None
        @rtype:None
        """

        self.positional_only = positional_only or []
        self.positional_default = positional_default or {}
        self.varargs = varargs
        self.kwonly = kwonly or []
        self.kwonly_default = kwonly_default or {}
        self.varkwargs = varkwargs

    def __iter__(self):
        return iter(self.args)

    def __contains__(self, arg):
        return arg in self.args

    @property
    def args(self):

        args = self.positional_only[:]
        args.extend(self.positional_default.keys())
        if self.varargs:
            args.append(self.varargs)
        args.extend(self.kwonly)
        args.extend(self.kwonly_default.keys())
        if self.varkwargs:
            args.append(self.varkwargs)
        return args

    def parse_args(self, args):
        """
        @param args: variant containing args
        @type args: variant
        @return: None
        @rtype: None

        Parse unknown type to build args from string/list/etc.
        """

        # Check things one by one, return as soon as match
        # is found.

        if isinstance(args, str):
            self.parse_from_string(args)
            return

        # dict/mapping type?

        try:
            for k, v in args.items():
                self._update_kw_arg(k, v)
            return
        except TypeError:
            pass

        # iterable yielding strings?
        for arg in args:
            self.parse_from_string(arg)

    def parse_kw_arg_str(self, arg: str):

        kw, val = arg.split('=')
        self._update_kw_arg(kw, val)

    def _update_kw_arg(self, kw, val):
        # if kw was a kwonly arg, user probably wants to just
        # update it, so try that and fallback on assigning to positional
        if kw in self.kwonly_default:
            self.kwonly_default[kw] = val
        else:
            self.positional_default[kw] = val

    def parse_from_string(self, args: str):
        """
        @param args: String containing arg or args(?)
        @type args: string
        @return: None
        @rtype: None

        Parse a string to add args to self from string.
        Let this function handle all logic related to
        parsing a string for args.

        When finding args with default values, assume
        positional default arg types.

        This function got super ugly really fast.
        It should probably be completely redone, but the
        ugly code was already part of an unneeded
        premature optimization for convenience.
        """

        if ',' in args and '=' not in args:
            self.positional_only.extend(args.split(','))

        elif ',' in args and '=' in args:

            arg_list = args.split(',')

            # repair broken eg split ('x'=(1,2,3))
            # this doesn't work on nested parenthesis
            # also, this mess is why C has goto

            # Outer while loop only exists as a goto substitute
            # first for loop loops through whole arg_list for malformed args
            # inner for loop scans for ')' match to broken arg
            # if found, loop needs to entirely reset because we modified the list
            # significantly while iterating, but we have to break out of two loops
            # so raise StopIteration to signal the outer for loop to break and reset.
            # If fix is not found, raise a ProxyError.
            # if we never find anything to fix, the outer for loop breaks out of the while.
            # This would be much cleaner with a single goto from 'raise StopIteration' to just
            # before the first for loop. oh well.
            while True:
                for i, arg in enumerate(arg_list):
                    if '(' in arg and ')' not in arg:
                        try:
                            for n, nextarg in enumerate(arg_list[i:], start=i):
                                if ')' in nextarg and '(' not in nextarg:
                                    fixed_args = ', '.join(arg_list[i:n + 1])
                                    del arg_list[i:n + 1]
                                    arg_list[i] = fixed_args
                                    raise StopIteration
                            else:
                                raise ProxyError("Malformed arg string.\n%s" % args)
                        except StopIteration:
                            break
                else:
                    break

            # This code has to be repeated here, because if we did a recursive call to
            # the function, it would trip the above block again and get stuck in an infinite loop.

            for arg in args:
                if '=' in arg:
                    self.parse_kw_arg_str(arg)
                elif '**' in arg:
                    self.varkwargs = arg.strip('**')
                elif '*' in arg:
                    self.varargs = arg.strip('*')
                else:
                    self.positional_only.append(arg)

        elif '=' in args:
            self.parse_kw_arg_str(args)
        elif '**' in args:
            self.varkwargs = args.strip('**')
        elif '*' in args:
            self.varargs = args.strip('*')
        else:
            self.positional_only.append(args)

    @property
    def ArgString(self):
    
        pos_only_string = ', '.join(self.positional_only)
        pos_default_string = ', '.join("%s=%s" % (arg, val)
                                       for arg, val in self.positional_default.items())
        vararg_string = ("*" + self.varargs) if self.varargs else ''
        kwonly_string = ', '.join(self.kwonly)
        kwonly_default_string = ', '.join("%s=%s" % (arg, val)
                                          for arg, val in self.kwonly_default.items())
        varkwargs_string = ("**" + self.varkwargs) if self.varkwargs else ''
    
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


class ProxyBase():
    """ Eventually it makes more sense to have function, method, class
    be sublcasses of proxy base, since there's a lot of overlap
    """

    __slots__ = [
                'name',
                'args',
                'doc',
                'decorators',
                'ide_comments'
                ]

    def __init__(self,
                 name: str,
                 args: ArgsProxy=None,
                 doc: str=None,
                 decorators: list=None,
                 ide_comments: list=None):

        """
        @param name: Name of the proxy
        @type name: string
        @param args: Args() instance of args function should accept
        @type args: ArgsProxy
        @param doc: docstring, if any
        @type doc: string
        @param decorators: decorators to include before function def
        @type decorators: list of decorators
        @param ide_comments: comments eg pynoinspection
        @type ide_comments: list
        """

        self.name = name

        if not isinstance(args, ArgsProxy):
            if args is None:
                args = ArgsProxy()
            else:
                tmp = args
                args = ArgsProxy()
                args.parse_args(tmp)

        self.args = args
        self.doc = doc or ''
        self.decorators = decorators or []
        self.ide_comments = ide_comments or []


class FunctionProxy(ProxyBase):
    """ Proxy object to more intuitively assign
    attributes for interpretation by ClassWriter
    """

    __slots__ = [
        'body',
        'ret'
        ]

    # noinspection PyTypeChecker
    def __init__(self,
                 name: str='',
                 body: list=None,
                 ret: str=None,
                 **kwargs):

        """
        @param name: Name of the function
        @type name: string
        @param args: Args() instance of args function should accept
        @type args: ArgsProxy
        @param doc: docstring, if any
        @type doc: string
        @param body: the function body, if any.list of coherent code segments (eg statements)
        @type body: list
        @param ret: name of return variable, as defined in class body
        @type ret: variant
        @param decorators: decorators to include before function def
        @type decorators: list of decorators
        @param IDEcomments: comments eg pynoinspection
        @type IDEcomments: list
        """
        kwargs['name'] = name
        super().__init__(**kwargs)

        self.body = body or ['pass']
        self.ret = ret or ''

    def addArgs(self, args: list):
        self.args.parse_args(args)

    def addArg(self, arg: str):
        self.args.parse_args(arg)

    def addKwArgs(self, args: dict):
        self.args.parse_args(args)


class MethodProxy(FunctionProxy):

    __slots__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'self' not in self.args:
            self.args.positional_only.insert(0, 'self')


class ClassProxy(ProxyBase):
    """ Proxy for class definition.
    """

    __slots__ = [
                'bases',
                'metaclass',
                'classvars',
                'methods'
                ]

    def __init__(self,
                 name: str,
                 bases: tuple=None,
                 metaclass: str='',
                 classvars: list=None,
                 methods: dict=None,
                 **kwargs):
        """

        @param name: class name
        @type name: string
        @param bases: tuple of bases
        @param metaclass: name of metaclass

        @param doc: class docstring
        @type doc: string
        @param classvars: list of classvariables
        @type classvars: list of 2-tuples of variablename, value
        @param methods: dict of name:FunctionProxy
        @type methods: dict

        """

        # noinspection PyNoneFunctionAssignment
        args = kwargs.pop('args', None)
        kwargs['name'] = name
        super().__init__(**kwargs)

        self.name = name
        self.bases = bases or []
        self.metaclass = metaclass or ''

        self.classvars = classvars or []
        self.methods = methods or {}

        if args:
            init = MethodProxy(name='__init__',
                               args=args)
            self.methods.insert(0, init)

    @property
    def decorator_strings(self) -> str:
        if self.decorators:
            return '\n@'.join(self.decorators).join(('@', '\n'))

    @property
    def class_declaration(self) -> str:
        dec = "class %s(%s%s)"
        name = self.name
        bases = self.bases
        metaclass = self.metaclass

        base_string = ','.join(bases) if bases else ''
        meta_string = 'metaclass=' + metaclass

        if base_string and meta_string:
            dec_args = ', '.join((base_string, meta_string))
        else:
            dec_args = base_string + meta_string

        return ''.join((
            'class',
            name,
            '(',
            dec_args,
            '):'
        ))

    def addMethod(self, method: FunctionProxy):
        """
        @param method: method to add
        @type method: FunctionProxy
        @return: None
        @rtype: None
        """
        self.methods[method.name] = method
