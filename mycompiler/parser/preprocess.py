"""

Created by: Nathan Starkweather
Created on: 02/15/2014
Created in: PyCharm Community Edition


"""
from re import compile as re_compile, MULTILINE
import re


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
