"""

Created by: Nathan Starkweather
Created on: 04/03/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'

from os import listdir


# noinspection PyUnresolvedReferences
def dirwalk(dir):
    contents = listdir(dir)
    paths = []; path_append = paths.append
    for f in contents:
        path = join((dir, f))
        try:
            paths.extend(dirwalk(path))
        except OSError:
            path_append(path)
    return paths


