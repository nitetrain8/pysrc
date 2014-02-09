
'''

Created by: Nathan Starkweather
Created on: 02/08/2014
Created in: PyCharm Community Edition


'''
__author__ = 'Nathan Starkweather'

from .uicfg import load_cfg
from .basecfg import rebuild_cfg

try:
    cfg_ops = load_cfg()
except:
    rebuild_cfg()
    cfg_ops = load_cfg()

