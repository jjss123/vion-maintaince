# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-08-03 18:05:46
# @Last Modified by:   hylide
# @Last Modified time: 2016-08-03 18:05:59

from lxml import etree

class XmlTree(object):
    ''''''

    def __init__(self, fp):
        self.tree = etree.parse(fp)
        self.root = self.tree.getroot()



class DictStruct(object):
    ''''''

    def __init__(self):
        pass

