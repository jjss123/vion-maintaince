# -*- coding: utf-8 -*-
'''
   module: state_collect
'''
# @Author: riposa
# @Date:   2016-05-30 14:53:52
# @Last Modified by:   riposa
# @Last Modified time: 2016-06-30 16:52:25

import platform
import os
import commands
import json
import re

from rec_log import record

def get_command_return(cmd, callback=None):
    '''
        function:  get_command_return
        parameter: cmd, commands to be executed.
                   callback, func to deal with result


                    of the commands, if exists.
        return:    tuple, combined with status and output, after commands
                   executed.
                   unknown type, determined by the callback function, if
                   exist
    '''

    status, output = commands.getstatusoutput(cmd)
    if callback:
        return callback(status, output)
    return (status, output)

@record(module='colon_callback', description='callback deal with colon ":"')
def colon_callback(status, output):
    '''
        function:   colon_callback
        parameter:  status, after executed command, the status you got.
                    output, the output string you got.
        return:     tuple, combined with status and transformed output.
                    or some other types.
    '''

    output_dict = dict()
    for li in output.splitlines():
        if ':' in li:
            key = li.split(':')[0].replace(' ','').replace('\t','')
            value = li.split(':')[1].replace(' ','').replace('\t','').replace('\n')
            output_dict[key] = value
    return json.dumps(output_dict)

@record(module='net_callback', description='callback deal with /proc/net/tcp or udp output')
def net_callback(status, output):
    '''
        function:   net_callback
        parameter:  status, after executed command, the status you got.
                    output, the output string you got.
        return:     tuple, combined with status and transformed output.
                    or some other types.
    '''
    key = ['local_address', 'rem_address', 'cmdline']
    output_dict = dict()
    tmp = output.splitlines()[1:]
    for i in tmp:
        tmpl = i.split(' ')
        tmpli = list()
        for j in tmpl:
            if j != '':
                tmpli.append(j)
        output_dict[tmpli[0].split(':')[0]] = {key[0]:tmpli[1], key[1]:tmpli[2], key[2]:(tmpli[-3] + tmpli[-1])}
    return json.dumps(output_dict)

@record(module='ifconfig_callback', description='callback deal with ifconfig output')
def if_callback(status, output):
    '''
        function:   if_callback
        parameter:  status, after executed command, the status you got.
                    output, the output string you got.
        return:     tuple, combined with status and transformed output.
                    or some other types.
    '''
    ip_exp = '((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))'
    re_exp = {
        'ip': 'inet addr:' + ip_exp,
        'mask': 'Mask:' + ip_exp,
        'hwaddr': 'HWaddr ([0-9a-fA-F]{2})(([/\s:-][0-9a-fA-F]{2}){5})'
    }
    ip = re.findall(re_exp['ip'], output).group(0)
    mask = re.findall(re_exp['mask'], output).group(0)
    hwaddr = re.findall(re_exp['hwaddr'], output).group(0)

'''
class BaseInfo(object):
    '''
        Base Class for getting kinds of information
        base attribute:
            _cpu, usage of every cpu core.
            _cpui, cpu hardware info.
            _mem, total memory.
            _net, base info from ifconfig
            _block, disk info from df.
            _sys, system type and version.
    '''

    @classmethod
    def
'''

if __name__ == '__main__':
    print get_command_return('cat /proc/net/tcp', net_callback)

