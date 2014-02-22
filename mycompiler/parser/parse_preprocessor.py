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


if __name__ == '__main__':
    import re
    directive_re = r"^\s*#\s*([a-zA-Z]*)\s"
    ptrn = re.compile(directive_re)

    myfile = "C:\\Users\\Administrator\\Csrc\\pbsbkup\\sigecho.h"
    with open(myfile, 'r') as f:
        txt = f.readlines()

    matches = [(lineno, match.group(1)) for lineno, match in enumerate((ptrn.match(line) for line in txt)) if match]

    for lineno, directive in matches:
        print(lineno, directive)
        if directive not in directives:
            raise ValueError(directive)
