"""

Created by: Nathan Starkweather
Created on: 02/15/2014
Created in: PyCharm Community Edition


"""
import os
import re
directives = {
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


class Directive():

    VALID_DIRECTIVES = directives

    def __init__(self):
        """
        """
        pass


def parse(stream):
    """
    @param stream: io.IOBase
    @type stream: io.IOBase
    @return: list[T]
    @rtype: list[T]
    """




if __name__ == '__main__':
    valid_id = r"[a-zA-Z_][a-zA-Z_0-9]"

    directive_re = r"^\s*#\s*([a-zA-Z]*)\s"
    ptrn2 = r"^\s*#\s*([a-zA-Z]*\s*?\n|.*?[^\\]\n)"

    ptrn3 = r"^\s*#\s*({id}*?\n)".format(id=valid_id)
    ptrn4 = r"^\s*#\s*({id}*?)\s+({id}*?)\n".format(id=valid_id)
