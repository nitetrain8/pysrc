"""

Created by: Nathan Starkweather
Created on: 02/27/2014
Created in: PyCharm Community Edition


"""
from os.path import exists as _exists, splitext as _splitext

__author__ = 'Nathan Starkweather'


def unique_name(fpath):
    """
    Make a unique name for the filepath by stripping extension,
    and adding 1, 2... to the end until a unique name is generated.

    @param fpath: filepath to make unique name for
    @type fpath: str
    @return: str
    @rtype: str
    """
    if not _exists(fpath):
        return fpath

    split_path = _splitext(fpath)
    i = 1
    tmplt = "(%d)".join(split_path)
    new = tmplt % i
    while _exists(new):
        i += 1
        new = tmplt % i
    return new
