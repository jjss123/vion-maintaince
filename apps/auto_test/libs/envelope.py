# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-07-15 11:12:15
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-15 17:58:46
'''
    module for constructing soap request and resolve soap post
'''

import xml.etree.cElementTree as ET
import json


class SoapEnvelopeTree(object):
    '''
        Soap Envelope Tree parser
    '''

    def __init__(self, envString):

        if not envString:
            # construct new envelope xml tree
            root = ET.Element('SOAP-ENV:Envelope')
            root.set('xmlns:SOAP-ENV', 'http://schemas.xmlsoap.org/soap/envelope/')
            root.set('xmlns:SOAP-ENC', 'http://schemas.xmlsoap.org/soap/encoding/')
            root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
            root.set('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")
            root.set('xmlns:vtns', "http://tempuri.org/vtns.xsd")
            ET.SubElement(root, 'SOAP-ENV:Body')
            self.root = root
            self.tree = ET.ElementTree(root)

        else:
            self.root = ET.fromstring(envString)

    def set_sub_element(self, father, tag, text=None, attrib=None):
        '''
            add sub element to the specific father tag
        '''

        father_el = [ i for i in self.root.iter(father)][0]
        if type(father_el) == None:
            return ('error', 'can not find the node')
        child = ET.SubElement(father_el, tag)
        if text:
            child.text = text
        if attrib:
            for i in attrib.keys():
                child.set(i, attrib[i])

        return 0

    def get_post_content(self):
        '''
            get the soap post content(json) by resolving xml string
        '''

        try:
            err_el = [ i for i in self.root.iter('SOAP-ENV:Fault')][0]
            return ('error', err_el.find('faultstring').text)
        except IndexError:
            a = [j for j in self.root.iter('result')][0]
            try:
                return ('success', json.loads(a.text))
            except ValueError:
                return ('success', a.text)

def soap_request(url, method, param=None):
    with open('header.conf') as head_file:
        head = json.loads(head_file.read().replace(r'%url%', url))

    env_tree = SoapEnvelopeTree(None)
    env_tree.set_sub_element('SOAP-ENV:Body', 'vtns:%s' % method, None, None)
    if param:
        for i in param.keys():
            env_tree.set_sub_element('vtns:%s'% method, i, param[i], None)
    
    data = '<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(env_tree.root, encoding='utf-8')

    return (head, data)

def resolve_post(response):
    response = response.replace('&#xA;', '')
    env_tree_post = SoapEnvelopeTree(response)
    (status, content) = env_tree_post.get_post_content()

    return content

if __name__ == "__main__":
    (head, data) = soap_request('192.168.9.106', 'GetDeviceInfo', {'deviceSerialNums':'vion-master', 'nDeviceInfoType':'0', 'bGroup': 'true'})
    print 'POST', '/', data, head
    print data
    (head, data) = soap_request('192.168.9.106', 'UpgradeSoftware', {'deviceSerialNums': 'Group1',
                                                    'packagePath': '/usr/local/VionSoftware/Vmts/files/QServer_LINUX-ARM-TK1_2.4.1-dengzc-20160805.tar.gz',
                                                    'bGroup': 'true'})
    print head,data