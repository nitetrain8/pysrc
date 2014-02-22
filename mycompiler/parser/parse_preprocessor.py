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
        txt2 = f.read()
        txt = txt2.splitlines()

    ptrn2 = re.compile(r"^\s*#\s*([a-zA-Z]*\s*?\n|.*?[^\\]\n)", re.MULTILINE)
    valid_id = r"[a-zA-Z_][a-zA-Z_0-9]"
    ptrn3 = r"^\s*#\s*({id}*?\n)".format(id=valid_id)
    ptrn4 = r"^\s*#\s*({id}*?)\s+({id}*?)\n".format(id=valid_id)

    matches = [(lineno, match.group(1)) for lineno, match in enumerate((ptrn.match(line) for line in txt)) if match]
    matches2 = [match for match in re.findall(ptrn4, txt2, re.MULTILINE)]
    # for lineno, directive in matches:
    #     print(lineno, directive)
    #     if directive not in directives:
    #         raise ValueError(directive)
    for match in matches2:
        print(match)
