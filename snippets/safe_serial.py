"""

Created by: Nathan Starkweather
Created on: 02/10/2014
Created in: PyCharm Community Edition

Convenience functions to safely serialize an object
and write to file without accidentally truncating the file
if an error is thrown during the serialization process.

Write to temp file (StringIO instance) to throw any errors
during process. Once temp file is written, open file and
write the temp file contents.
"""
__author__ = 'Nathan Starkweather'

from pickle import dump as pickle_dump
from io import StringIO, BytesIO
from json import dump as json_dump


def safe_pickle(obj: object, filename: str, **kwargs):
    temp = BytesIO()
    pickle_dump(obj, temp, **kwargs)

    with open(filename, 'wb') as f:
        f.write(temp.getvalue())


def safe_json(obj: object, filename: str, **kwargs):
    temp = StringIO()
    kwargs['indent'] = kwargs.get('indent', 4)
    json_dump(obj, temp, **kwargs)

    with open(filename, 'w') as f:
        f.write(temp.getvalue())

