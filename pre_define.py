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


@singleton
class GlobalVar(object):

    region = []

    def __init__(self):
        pass

    def list(self):
        """
        show current global variables
        :return: <dict>
        """
        res = dict()
        for i in dir(GlobalVar):
            m = re.match(r"^[_GlobalVar__]\w+[^__]$", i)
            if m:

                res[i.replace('_GlobalVar__', '')] = getattr(GlobalVar, i)
        return res

    def set(self, params, src):
        """
        set global variables
        :param params: <dict>
        :return: <Boolean>
        """

        for i in params.keys():
            setattr(GlobalVar, '_GlobalVar__' + i + "::" + src, params[i])

        return True

    def get(self, *attrs):
        """
        get global variables
        :param attrs:
        :return:
        """

        if not attrs:
            return self.list()

        res = {}
        for i in attrs:
            try:
                for j in GlobalVar.region:
                    try:
                        tmp_res = GlobalVar.__getattribute__('_GlobalVar__' + i + '::' + j)
                    except:
                        pass
                    if res.has_key(i):
                        res[i].append(tmp_res)
                    else:
                        res[i] = tmp_res
            except AttributeError:
                raise Exception('')

        return res


def load_config():
    pass

if __name__ == '__main__':
    a = GlobalVar()
    print a.set({"test": 1, "tt": 2}, 'region1')
    print GlobalVar
    print dir(GlobalVar)
    print a.list()
    print a
    b = GlobalVar()
    print b.get("test", "tt")