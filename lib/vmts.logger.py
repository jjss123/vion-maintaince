# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 10:08:06
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:23:57

import os
import logging
import logging.handlers

from pre_define import GlobalVar as cfg


def singleton(cls):
    instances = {}

    def _singleton(*args, **kw):

        if cls not in instances:
            instances[cls] = {args[0]: cls(*args, **kw)}
        else:
            if args[0] not in instances[cls]:
                instances[cls][args[0]] = cls(*args, **kw)

        print instances
        return instances[cls][args[0]]
    return _singleton

@singleton
class VmtsLogger(object):
    """

    """

    formatter = '%(levelname)s - %(asctime)s %(name)s: %(message)s'
    formmater_debug = '%(levelname)s - %(asctime)s %(name)s: %(message)s\n\tCall Stack Info:\n\t\tfunction: ' \
                      '%(funcName)s\n\t\tmodule: %(module)s\n\t\tfile: %(pathname)s'

    def __init__(self, name, level='INFO',
                 base_dir=os.path.dirname(__file__) + '../log/'):
        """"""
        self.name = name
        self.level = level.upper()
        self.fp = base_dir + name + '.log'

        fileHandle = logging.handlers.TimedRotatingFileHandler(self.fp, when='D', backupCount=5, encoding='utf-8')
        consoleHandle = logging.StreamHandler()

        if cfg.

if __name__ == "__main__":
    test = VmtsLogger('test', 'INFO')
    test1 = VmtsLogger('test', 'INFO')
    test2 = VmtsLogger('test1', 'INFO')


