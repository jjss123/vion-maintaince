# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 10:08:06
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:23:57
import re

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


#@singleton
class GlobalVar(object):
    __b =1

    def __init__(self):
        pass

    def list(self):
        '''
        show current global variables
        :return: <dict>
        '''
        res = dict()
        for i in dir(GlobalVar):
            m = re.match(r'^[_GlobalVar__]\w+[^__]$', i)
            if m:

                res[i.replace('_GlobalVar__','')] = getattr(GlobalVar, i)
        return res


    def set(self, params):
        '''
        set global variables
        :param params: <dict>
        :return: <Boolean>
        '''

        for i in params.keys():
            setattr(GlobalVar ,'_GlobalVar__' + i, params[i])

        return True


    def get(self, *attrs):
        '''
        get global variables
        :param attrs:
        :return:
        '''

        if not attrs:
            return GlobalVar.list()

        res = dict()
        for i in attrs:
            res[i.replace('_GlobalVar__','')] = GlobalVar.__getattribute__(GlobalVar, '_GlobalVar__' + i)

        return res


if __name__ == '__main__':
    a = GlobalVar()
    print a.set({"test":1, "tt": 2})
    print GlobalVar
    print dir(GlobalVar)
    print a.test
    print a.list()
