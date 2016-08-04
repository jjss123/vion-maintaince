# -*- coding: utf-8 -*-
'''
   module: state_collect
'''
# @Author: riposa
# @Date:   2016-05-30 14:53:52
# @Last Modified by:   riposa
# @Last Modified time: 2016-06-30 16:52:25


import commands
import sys


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


def colon_callback(status, output):
    '''
        function:   colon_callback
        parameter:  status, after executed command, the status you got.
                    output, the output string you got.
        return:     dict, combined with status and transformed output.
                    or some other types.
    '''
    if not status:

        output_dict = dict()
        for li in output.splitlines():
            if ':' in li:
                key = li.split(':')[0].strip()
                value = li.split(':')[1].strip()
                output_dict[key] = value
        return output_dict
    else:
        return False

def cpuinfo_callback(status, output):
    '''
    :param status: after executed command, the status you got.
    :param output: the output string you got.
    :return: type::dict
    '''
    if not status:

        output_dict = dict()
        group_no = 0
        flag = True
        sect = dict()
        for li in output.splitlines():
            if flag:
                if ':' in li:
                    key = li.split(':')[0].strip()
                    value = li.split(':')[1].strip()
                    sect[key] = value
                else:
                    flag = False
            else:
                if ':' in li:
                    if 'Hardware' in li:
                        key = li.split(':')[0].strip()
                        value = li.split(':')[1].strip()
                        output_dict[key] = value
                        continue
                    output_dict['core ' + str(group_no) ] = sect
                    sect = dict()
                    key = li.split(':')[0].strip()
                    value = li.split(':')[1].strip()
                    sect[key] = value
                    flag = True
                    group_no += 1
        return output_dict
    else:
        return False

def private_version_callback(status, output):
    if not status:
        output_dict = dict()
        flag = ''
        for li in output.splitlines():
            if 'u-boot' in li:
                flag = 'u-boot'
                sect = dict()
                continue
            if 'kernel' in li:
                flag = 'kernel'
                sect = dict()
                continue
            if flag:
                if ':' not in li:
                    output_dict[flag] = sect
                    flag = ''
                if ':' in li:
                    key_sect = li.split(':')[0].strip()
                    sect[key_sect] = li.split(':')[1].strip()
        output_dict[flag] = sect
        return output_dict
    else:
        return False

def space_callback(status, output):
    if not status:
        output_dict = dict()
        line_no = 0
        for li in output.splitlines():
	    params = list()
            tmp = [i.strip() for i in li.strip().split(' ')]
	    for i in tmp:
	        if i == '':
		    pass
		else:
		    params.append(i)
	    if params[-1] == 'on':
		params[-2] = 'Mounted on'
		params.pop()
            output_dict[line_no] = params
	    line_no += 1

        return output_dict
    else:
        return False

if __name__ == '__main__':
    if sys.argv[2] == 'colon_callback':
        print get_command_return(sys.argv[1], colon_callback)
    elif sys.argv[2] == 'private_version_callback':
        print get_command_return(sys.argv[1], private_version_callback)
    elif sys.argv[2] == 'space_callback':
        print get_command_return(sys.argv[1], space_callback)
    elif sys.argv[2] == 'cpuinfo_callback':
        print get_command_return(sys.argv[1], cpuinfo_callback)

