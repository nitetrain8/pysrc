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


def filter_directives(stream, magic=directive_re.match):
    """
    @param stream: file-like object supporting iteration
    @type stream: typehint.FileObject
    @return: yield complete lines corresponding to directives.
    @rtype: __generator[str]
    """
    s = iter(stream)
    for line in s:
        match = magic(line)
        if match:
            d, *args = match.groups()
            # can't use takewhile generator here-
            # otherwise, a line would be skipped when
            # takewhile calls a line and returns false, but
            # doesn't rewind iterator by 1.
            while args[-1].endswith('\\'):
                try:
                    #: @type: str
                    line = next(stream, '')
                except StopIteration:
                    raise InvalidDirective("Invalid trailing '\\' in token at end of file")
                # print("--line--", repr(re.sub(r"(^\s+)(\S.*)(\s+\\$)", '', line)))

                args.append(line)
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

    from subprocess import call
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

    call(args)

    from os import startfile
    try:
        startfile(outfile)
    except FileNotFoundError:
        pass
