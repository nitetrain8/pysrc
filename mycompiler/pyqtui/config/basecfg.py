"""

Created on Jan 12, 2014

C:/Users/Administrator/Documents/Programming/PythonSource/source/mycompiler/pyqtui/test2.py
@author: Nathan S.

Rebuild default config file settings from hard-coded defaults.
Provide access to hard-coded defaults if desired.
"""

import json
from itertools import chain
from os.path import dirname as path_dirname, exists as path_exists
from collections import OrderedDict

jsonfile = '/'.join((path_dirname(__file__), 'uicfg.json'))
JSON_INDENT = 4


def default_cflags():
    """
    @return: mapping of cflags categories to list of specific flags
    @rtype: dict
    """

    standard = ["-Wall", '-Wextra', '-std=c11']
    warnings = ["-Wall", '-Werror', '-Wextra', '-Wfatal-errors', '-Wpedantic', '-Wshadow', '-Wpointer-arith',
                '-Wcast-qual', '-Wmissing-prototypes', '-Wstrict-prototypes', '-Wuninitialized', '-Wstrict-aliasing',
                '-Wcast-align', '-Wformat=2', '-Wmissing-declarations']
    language = ['-std=c11', '-std=c99', '-std=c90', '-ansi']
    optimization = ["-O1", "-O2", "-O3"]
    output = ['-c', '-S', '-E']

    flags = (
            standard,
            warnings,
            language,
            optimization,
            output
            )

    # Unique elements from above. Preserve order so they're categorically organized.
    All_ = OrderedDict()
    for flag in chain.from_iterable(flags):
        All_[flag] = None  # dummy, only need key
    All = All_.keys()

    cFlags = {
        'Standard': standard,
        'Warnings': warnings,
        'Language': language,
        'Optimization': optimization,
        'Compiler Output': output,
        'All': All
    }

    return cFlags


def default_cfg():
    """
    @return: mapping of config file sections
    @rtype: dict

    Call specific functions default functions to
    build the full dict of default config options.

    """
    cfg_ops = {
                'cFlags' : default_cflags()
                }

    return cfg_ops


def rebuild_cfg():
    """
    @return: None
    @rtype: None

    Rebuild the config file from hardcoded defaults. Overrides
    any existing file!
    """
    cfg = default_cfg()

    with open(jsonfile, 'w') as f:
        json.dump(cfg, f, indent=JSON_INDENT)


def cfg_exists():
    return path_exists(jsonfile)


if __name__ == '__main__':
        rebuild_cfg()



