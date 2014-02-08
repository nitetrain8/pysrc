__author__ = 'Nathan Starkweather'
'''

Created by: Nathan Starkweather
Created on: 02/01/2014
Created in: PyCharm Community Edition


'''


def printdir(obj):
    '''
    @param obj: any python object
    @type obj: variant
    @return: None
    @rtype: None
    '''
    for attr in dir(obj):
        try:
            print(attr, getattr(obj, attr))
        except Exception as error:
            print(error)

