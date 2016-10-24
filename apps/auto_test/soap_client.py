# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-07-15 14:48:29
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-15 17:02:12
'''module for send and recv soap message'''

import httplib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from envelope import soap_request, resolve_post

def call(url, port, method, param=None):
    (head, data) = soap_request(url, method, param)

    http_client = httplib.HTTPConnection(url, port, timeout=5)
    http_client.request('POST', '/', data, head)
    try:
        response = http_client.getresponse()
    except httplib.BadStatusLine:
        print 'illegal params cause no response'

    print response.read().replace('&#xA;', '')

    result = response.read()
    http_client.close()

    return result

if __name__ == '__main__':
    config = r'root\设备信息\网络信息\内网IP'.encode('utf-8')
    #print config
    import time
    #print call('192.0.12.101', 8850, 'GetVersion', None)
    a =call('192.168.9.106', 10030 , 'GetDeviceInfo',
               {'deviceSerialNums': 'Star-Device-192.168.5.3', 'nDeviceInfoType': '0', 'bGroup': 'false'})

    print a

    #res = call('192.168.9.106', 'UpgradeSoftware', {'deviceSerialNums':'Star-Cluster-109', 'packagePath':'/usr/local/VionSoftware/Vmts/files/QServer_LINUX-ARM-TK1_2.4.0-dengzc-20160804.tar.gz', 'bGroup':'false'})
    #res = call('192.168.9.106', 'UpgradeSoftware', {'deviceSerialNums': 'Star-Cluster-2;Star-Cluster-109',
                                                   # 'packagePath': '/usr/local/VionSoftware/Vmts/files/OperateServer_LINUX-ARM-TK1_0.1.3.59831.tar.gz',
                                                   # 'bGroup': 'false'})
    #res = call('192.168.9.106', 'UpgradeSoftware', {'deviceSerialNums': 'Group1',
                                                   # 'packagePath': '/usr/local/VionSoftware/Vmts/files/QServer_LINUX-ARM-TK1_2.4.1-dengzc-20160805.tar.gz',
                                                   # 'bGroup': 'true'})

    #print call('192.168.9.106', 'ControlDevice', {'deviceSerialNums':'Star-Cluster-192.168.5.2', 'szCommandInfo':'restartSoftService', 'szCommandParam':'QServer', 'bGroup':False})

    #print call('192.168.9.106', 'GetVersion')

    #print call('192.0.11.105', 'GetDeviceInfo', {'deviceSerialNums':'vion-master', 'nDeviceInfoType':'0'})
    #res = call('192.0.11.105', 'ExportConfigs', {'deviceSerialNum': 'vion-master', 'configName': config, 'softServiceName': 'OperatServer'})
    #print call('192.168.9.106', 'GetHSCConfig', {'deviceSerialNum': 'Star-Cluster-109', 'configName': config, 'softServiceName': 'OperatServer'})
    #while True:
    #    time.sleep(3)
    #    print call('192.168.9.106','GetUpgradeProgress', {'deviceSerialNums': 'Group1','packagePath': '/usr/local/VionSoftware/Vmts/files/OperateServer_LINUX-ARM-TK1_0.1.4.59840.tar.gz', 'bGroup': 'true'})

    #print res
'''
    import time
    import chardet
    import os

    print chardet.detect('\xb2\xbb\xb4\xe6\xd4\xda')
    print '\xb2\xbb\xb4\xe6\xd4\xda'.decode('cp819').encode('cp936')
    while 1:
        time.sleep(1)
        res1 = call('192.168.9.106', 'GetUpgradeProgress', {'deviceSerialNums': 'Star-Cluster-109',
                                                            'packagePath': '/usr/local/VionSoftware/Vmts/files/QServer_LINUX-ARM-TK1_2.4.0-dengzc-20160804.tar.gz',
                                                            'bGroup': 'false'})
        print res1
        for i in res1.values()[0]:
            for j in i.keys():
                print j, i[j].encode('cp819')
                os.system('echo {c} >> test.log'.format(c=str(j + str(i[j]).encode('cp819'))))
    #print call('192.0.11.105', 'GetHSCConfig', {'deviceSerialNums': 'vion-master', 'configName': '', 'softServiceName': ''})'''
