''' This is the most godawful module in existance.
Reader beware.

'''


pfc_tracefile = r'C:/Users/Administrator/Documents/Programming/pfc_tracefile.txt'

pfc_ignore = ['write_code',
              '__init__',
              '__new__',
              '_pfc'
              ]


class HerpADerpError(Exception):
    pass


__pfc_tracefile = open(pfc_tracefile, 'w')


def pfc(func, tracefile=__pfc_tracefile):

    if func.__name__ in pfc_ignore:
        return func
    
    __pfcmsg = "%s called\n\n" % func.__qualname__
    
    def _pfc(*args, **kwargs):
        print(__pfcmsg)
        tracefile.write(__pfcmsg)
        return func(*args, **kwargs)

    return _pfc


def closefile():
    print("file closed!")
    global __pfc_tracefile

    __pfc_tracefile.close()

import atexit
atexit.register(closefile)


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
















