__author__ = 'Nathan Starkweather'
'''

Created by: Nathan Starkweather
Created on: 01/27/2014
Created in: PyCharm Community Edition


'''

from os.path import dirname as path_dirname, exists as path_exists
import json


def load_cfg():
    cur_dir = path_dirname(__file__)
    cfg_file = '/'.join((cur_dir, 'uicfg.json'))
    with open(cfg_file, 'r') as f:
        cfg_ops = json.load(f)
    return cfg_ops




if __name__ == '__main__':
    try:
        cfg = load_cfg()
    except:
        import basecfg
        basecfg.rebuild_cfg()
        cfg = load_cfg()

    print(cfg)
