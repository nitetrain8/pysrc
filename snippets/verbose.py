"""
This is the most godawful module in existance.
Reader beware.

"""
from io import StringIO
import atexit

__pfc_iobuffer = StringIO()
__pfc_tracefile = r'C:/Users/Administrator/Documents/Programming/pfc_tracefile.txt'
logfile = __pfc_tracefile

pfc_ignore = [
              '__init__',
              '__new__',
              'pfc_wrapper',
              'pfc'
              ]


def pfc(func):

    # avoid wrapping self
    if func.__name__ in pfc_ignore:
        return func

    buf = __pfc_iobuffer
    __pfcmsg = func.__qualname__ + " called\n\n"
    
    def pfc_wrapper(*args, **kwargs):
        nonlocal buf
        print(__pfcmsg)
        buf.write(__pfcmsg)
        return func(*args, **kwargs)
    return pfc_wrapper


def __commit_log():

    bv = __pfc_iobuffer.getvalue()
    if not bv:
        return

    with open(logfile, 'w') as f:
        f.write(bv)

atexit.register(__commit_log)


class VerboseDict(dict):
    def __getitem__(self, key, dict_getitem_=dict.__getitem__):
        print("Getting key %s." % key)
        return dict_getitem_(self, key)
    
    def __setitem__(self, key, value, dict_setitem_=dict.__setitem__):
        print("Setting key %s to %r." % (key, value))
        return dict_setitem_(self, key, value)
        
    def __delitem__(self, key, dict_delitem_=dict.__delitem__):
        print("Deleting key %s.")
        return dict_delitem_(self, key)
















