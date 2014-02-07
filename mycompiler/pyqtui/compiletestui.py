



from time import perf_counter as timer
from io import StringIO


testui = "C:/Python33/Lib/site-packages/PyQt5/myprojects/ui/testui.ui"
out = StringIO()


from PyQt5 import uic

with open(testui, 'r') as f:
    uic.compileUi(f, out)

print(out.getvalue())















