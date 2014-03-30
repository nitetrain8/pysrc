"""

Created by: Nathan Starkweather
Created on: 02/01/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'


def printdir(obj, hide_private=True, **printkwargs):
    """
    @param obj: any python object
    @type obj: variant
    @return: None
    @rtype: None
    """
    attrs = dir(obj)
    if hide_private:
        attrs = [a for a in attrs if not a.startswith('__')]
        if not attrs:
            print("No non-private attrs")

    for attr in attrs:
        try:
            print(attr, getattr(obj, attr), **printkwargs)
        except Exception as error:
            print(error, **printkwargs)

