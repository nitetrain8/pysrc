"""

Created by: Nathan Starkweather
Created on: 02/10/2014
Created in: PyCharm Community Edition

Convenience functions to safely serialize an object
and write to file without accidentally truncating the file
if an error is thrown during the serialization process.

Write to temp file (StringIO/BytesIO instance) to throw any errors
during process. Once temp file is written, open file and
write the temp file contents.
"""
__author__ = 'Nathan Starkweather'

from pickle import dump as pickle_dump
from io import StringIO, BytesIO
from json import dump as json_dump
from os import makedirs
from os.path import split as path_split, exists as path_exists


def safe_pickle(obj, filepath, **kwargs):
    """
    @param obj: Any pickleable object
    @type obj:  T
    @param filepath: filepath to save the pickle file
    @type filepath: str
    @param kwargs: dict of pickle kwargs
    @type kwargs: dict
    @return: None
    @rtype: None
    """
    temp = BytesIO()
    pickle_dump(obj, temp, **kwargs)

    tail, _ = path_split(filepath)
    if not path_exists(tail):
        makedirs(tail)

    with open(filepath, 'wb') as f:
        f.write(temp.getvalue())


def safe_json(obj: object, filepath: str, **kwargs):
    temp = StringIO()
    kwargs['indent'] = kwargs.get('indent', 4)
    json_dump(obj, temp, **kwargs)

    tail, _ = path_split(filepath)
    if not path_exists(tail):
        makedirs(tail)

    with open(filepath, 'w') as f:
        f.write(temp.getvalue())

