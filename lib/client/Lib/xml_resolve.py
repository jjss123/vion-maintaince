# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-08-03 18:05:46
# @Last Modified by:   hylide
# @Last Modified time: 2016-08-03 18:05:59

import codecs
from lxml import etree


def ins_check(func):
    '''
    decorator for checking xmltree obj instantiated ,or not
    :param func: <function>,function obj which is decorated
    :return: None
    '''

    def _ins_check(self, args):

        if not isinstance(self.tree, etree._ElementTree):
            raise Exception('Need instantiate the XmlTree Object first')
        return func(self, args)

    return _ins_check

class XmlTree(object):
    ''''''

    def __init__(self, fp, encoding='GBK'):
        '''
        XmlTree constructor,
        :param fp: <String>, xml file path
        :param encoding: <String>, xml encoding
        '''
        self.tree = None
        self.root = None

        if encoding.lower() == 'gbk':
            encoding = 'cp936'
        elif encoding.lower() == 'utf8':
            encoding = 'utf-8'
        self.encoding = encoding.lower()

        self.xml_tree_initiated = self._new(fp)

    def _new(self, fp):
        '''
        construct new xml tree object,
        if file path(fp) existed, read the xml file, and return True,
        if not existed, create the file, and return False,
        :param fp: <String>, xml file path
        :return: <Boolean>
        '''

        try:
            with open(fp, 'r') as xs:
                self.tree = etree.parse(xs)
            self.root = self.tree.getroot()
            return True
        except etree.XMLSyntaxError:
            with codecs.open(fp, 'r', encoding=('GBK' if self.encoding.lower() == 'cp936' else self.encoding)) as self.xml_file_handle:
                self.tree = etree.parse(self.xml_file_handle.read())
            self.root = self.tree.getroot()
            return True
        except IOError:
            self.xml_file_handle = codecs.open(fp, 'w', encoding=('GBK' if self.encoding.lower()=='cp936' else self.encoding))
            return False

    @ins_check
    def get_elements_by_xpath(self, xpath):
        '''
        get elements by using specific xpath string
        :param xpath: <String>, xpath string
        :return: <List>, <Element> nodes
        '''

        return self.tree.xpath(xpath)

    @ins_check
    def get_elements_by_tags(self, tags):
        '''
        get elements by using only one or serveral tags,
        Notes: this method using Depth First rule by default, and will include the root tag itself.
        :param tags: <List>, xml tag names, can not be duplicate
        :return: <List>, <Element> nodes
        '''

        result = list()
        # tag list de-duplication
        if type(tags) == list:
            tags = list(set(tags))
            for i in tags:
                for j in etree.ElementDepthFirstIterator(self.root, i, inclusive=False):
                    result.append(j)
        elif type(tags) == str:
            for i in etree.ElementDepthFirstIterator(self.root, tags, inclusive=False):
                result.append(i)

        return result

    @ins_check
    def get_elements_by_text(self, text, tags=None):
        '''
        get elements by using node text. The text here means keyword which was included by some node text,
        :param text: <String>, keyword
        :param tags: <List> or <String>, xml tag names, can not be duplicate
        :return: <List>, <Element> nodes
        '''

        result = list()

        def textIterator(tag=None):
            for j in self.tree.getiterator(tag=tag):
                if bool(j.text) and (text in j.text):
                    result.append(j)

        if tags:
            # tag list de-duplication
            tags = list(set(tags))
            for i in tags:
                textIterator(i)

            return result
        else:
            textIterator()

            return result

    @ins_check
    def write(self, fp, pretty_print=False):
        '''
        wrapper of etree._ElementTree.write() method
        :param fp: <String>, file path
        :param pretty_print: <Boolean>, output formatted xml
        :return: <Boolean>
        '''

        self.tree.write(file=fp, encoding=self.encoding, pretty_print=pretty_print)
        return True

    @ins_check
    def get_xpath_by_element(self, e):
        '''
        Returns a structural, absolute XPath expression to find the specific element.
        :param e: <Element Object>,
        :return: <String>, xpath expression
        '''

        return self.tree.getpath(e)

if __name__ == "__main__":
    fp = 'D:\\basic-conf\\1.xml'
    test = XmlTree(fp, encoding='GBK')
    print test.xml_tree_initiated
    print test.get_elements_by_text('192')
    print test.get_elements_by_tags('SceneInfo')
    print test.get_xpath_by_element(test.get_elements_by_text('192')[3])
    test.write('D:\\basic-conf\\1.xml')