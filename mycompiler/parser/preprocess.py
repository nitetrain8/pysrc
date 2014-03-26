"""

Created by: Nathan Starkweather
Created on: 02/15/2014
Created in: PyCharm Community Edition


"""
from re import compile as re_compile
import re

identifier = r"[a-zA-Z_]\w*?"


class PreprocessorError(SyntaxError):
    pass


class InvalidDirective(PreprocessorError):
    """
    Invalid preprocessor syntax
    """
    pass


class Directive():

    VALID = {
        "include",
        "define",
        "if",
        "error",
        "import",
        "undef",
        "elif",
        "using",
        "else",
        "ifdef",
        "endif",
        "ifndef",
        "pragma"
    }

    def __init__(self, directive):
        """
        @param directive: name of directive
        """

        self.isValid = directive in self.VALID
        self.directive = directive

    @classmethod
    def regex(cls):
        return "(%s)" % '|'.join(cls.VALID)


class FlowCtrl(Directive):

    VALID = {
        "if",
        "elif",
        "else",
        "endif",
        "ifdef",
        "ifndef"
    }


class Include(Directive):
    VALID = {'include'}


directive_re = re_compile(r"\s*#\s*(%s)\s+(.*)" % identifier)
cpp_filter = re_compile(r"^\s*#")
arg_re = re_compile(r"\s*#\s*([a-zA-Z_]\w*)(?:\s+(.*))?$")


def filter_directives(stream, is_cpp_line=cpp_filter.match, arg_parser=arg_re.match):
    """
    @param stream: file-like object supporting iteration
    @type stream: typehint.FileObject
    @return: yield complete lines corresponding to directives.
    @rtype: __generator[str]
    """

    rstrip = str.rstrip
    lines = map(rstrip, iter(stream))
    line = ''
    lineno = 0

    def next_line(is_cpp_line=is_cpp_line, _next=next):
        nonlocal line, lineno, lines
        try:
            while True:
                line = _next(lines)
                lineno += 1
                if is_cpp_line(line):
                    return True
        except StopIteration:
            return False

    while next_line():
            match = arg_parser(line)
            if not match:  # empty '#' by itself
                continue

            d, *args = match.groups()
            append = args.append
            while args[-1].endswith('\\'):
                #: @type: str
                line = next(stream, '')
                append(line[:-1])
            print(args)
            yield d, ' '.join(re.sub(r"(^\s*?)(\S.*?)(\s*\\\s*$)", '\\2', line) for line in args)


def parse_line(line, directive_re=re_compile(r"^\s*#\s*([a-zA-Z_][a-zA-Z_0-9]*)\s*(\(.*\))?\s*(.*?)(\\)?\n", re.DOTALL)):
    """
    @param line:
    @type line:
    @param directive_re:
    @type directive_re:
    @return:
    @rtype:
    """
    match = directive_re.match(line)
    if match:
        return match.groups()
    return match


def parse_stream(stream):
    """
    @param stream: io.IOBase
    @type stream: io.IOBase
    @return: list[T]
    @rtype: list[T]
    """

    # Ensure iterable file object
    stream_iter = iter(stream)
    for line in stream_iter:
        parse_line(line)


if __name__ == '__main__':
    valid_id = r"[a-zA-Z_][a-zA-Z_0-9]"

    directive_re = r"^\s*#\s*([a-zA-Z]*)\s"
    ptrn2 = r"^\s*#\s*([a-zA-Z]*\s*?\n|.*?[^\\]\n)"

    ptrn3 = r"^\s*#\s*({id}*?\n)".format(id=valid_id)
    ptrn4 = r"^\s*#\s*({id}*?)\s+({id}*?)\n".format(id=valid_id)

    from subprocess import call, check_output
    from os.path import dirname

    cfile = "C:\\Users\\Administrator\\Documents\\Programming\\python\\pysrc\\test\\test_mycompiler\\test_parser\\files\\base26.c"
    cdir = dirname(cfile)
    # fooh = cdir + "\\foo.h"
    #
    # with open(fooh, 'w') as f:
    #     f.write("#ifndef DUMMY_H\nfloat dummy;\n#endif \\\\DUMMY_H")
    CC = "D:\\MinGW\\mingw64\\bin\\gcc.exe -E"
    outfile = "C:\\foo.txt"
    args = "{CC} {cfile} -o {outfile}".format(CC=CC, cfile=cfile, outfile=outfile)

    with open("C:\\foo.txt", 'w') as f:
        f.truncate()

    result = check_output(args)
    print(result)
    if not result:
        from os import startfile
        try:
            startfile(outfile)
        except FileNotFoundError:
            pass
