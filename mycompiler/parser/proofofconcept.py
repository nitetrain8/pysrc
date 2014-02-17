"""

Created by: Nathan Starkweather
Created on: 02/15/2014
Created in: PyCharm Community Edition


"""

file = "C:\\Users\\Administrator\\Documents\\Programming\\python\\pysrc\\mycompiler\\parser\\helloworld.c"
file2 = "C:\\Users\\Administrator\\Csrc\\pbsbkup\\sigecho.h"
import re

with open(file2, 'r') as f:
    text = f.readlines()

ptrn = r"^#([a-zA-Z]+)\s"

obj = re.compile(ptrn)

re_cache = {
    "pp_token" : re.compile(ptrn),
    "include" : re.compile(r"^#include\s<(.*?)>")
}

i = re_cache['include']


matches = []
for line in text:
    try:
        matches.append(obj.match(line).group(1))
    except AttributeError:  # match returned None
        pass
# print(obj.match(text).group(0))

matches = [(i, match.group(1)) for i, match in enumerate((obj.match(line) for line in text)) if match]



def parse_define(line):
    pass

handlers = {
            'include' : parse_define
        }

for lineno, token in matches:
    if token == 'include':
        print(lineno, i.match(text[lineno]).groups())

# print(matches)
for lineno, token in matches:
    assert token in text[lineno]
