"""

Created by: Nathan Starkweather
Created on: 02/01/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'


def printdir(obj, **printkwargs):
    """
    @param obj: any python object
    @type obj: variant
    @return: None
    @rtype: None
    """
    for attr in dir(obj):
        try:
            print(attr, getattr(obj, attr), **printkwargs)
        except Exception as error:
            print(error, **printkwargs)

