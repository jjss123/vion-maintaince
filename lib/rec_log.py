# -*- coding: utf-8 -*-
'''
    log module

    usage:
        two kinds of log output called by decoration or function.
        log type = INFO:
            add '@rec_log.record(**kwargs)' on the method you want to record log.
            parameter support [module, description]
        log type = ERROR:
            add line - Recording.error(<%message%>)
'''
# @Author: riposa
# @Date:   2016-05-16 14:49:05
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-01 14:00:48

import logging
import logging.config
import sys
import time
import shutil
import os
import traceback

logging.config.fileConfig(sys.path[0] + '\\' + "logger.conf")

LOG_PATH = {
    'info': '../log/info.log',
    'error': '../log/error.log',
    'backup': '../log/backup/'
    }

def set_log_path(log_type, npath):
    '''
        method for setting log path
    '''


def record(**Keys):
    '''
            decoration of recording info log
            parameter:
                    **Keys, optional para, include module info and description
    '''

    def _deco(func):
        def __deco(*args, **kwargs):
            # combine all the value-typed and key-value-typed parameter to one
            # list

            try:
                res = func(*args, **kwargs)
                Recording.info(Keys, [args, kwargs], res)
                return res
            except:
                err = sys.exc_info()
                Recording.error(err)
        return __deco
    return _deco

def log_backup(log_type):
    '''
        backup log file by date.
        log_type = info or error
    '''

    try:
        shutil.move(LOG_PATH[log_type], LOG_PATH['backup'])
        os.rename(LOG_PATH['backup'] + '%s.log'%log_type, \
        LOG_PATH['backup'] + '%s.log'%(log_type + time.ctime()))
    except:
        err = sys.exc_info()
        Recording.error(err)



class Recording(object):
    '''
        recording class, include info and error class method
    '''

    def __init__(self):
        pass

    @classmethod
    def info(cls, keys, args, res):
        '''
                log level: info
                parameter:
                **Keys, optional para, include module info and description
                args, type:list,
                original parameter of function decorated by the decoration - "@record"
        '''
        # set basic config of logging module for new logfile

        logger_info = logging.getLogger('info')
        logger_info.setLevel(logging.INFO)
        if keys.has_key('module'):
            module = keys['module']
        else:
            module = 'unknown'
        if keys.has_key('description'):
            description = keys['description']
        else:
            description = 'unknown'
        # recombine log text
        if args:
            content = '\n\tin %s:\n\tEvent %s Done\n\tinput:\n\t\t%s' % (
                module, description, str('\t\t'.join(args[0]) + '\n\t\t' + str(args[1])))
            content = content + '\n\treturn: ' + str(res)
        else:
            content = 'in %s:\n\tEvent %s Done' % (module, description)
        # print content
        logger_info.info(content)

    @classmethod
    def error(cls, err):
        '''
                log level: error
                parameter:
                        None
        '''
        logger_error = logging.getLogger('error')
        logger_error.setLevel(logging.ERROR)

        err_type = err[0]
        err_value = err[1]
        ts_text = 'Traceback (most recent call last):\n'

        for filename, line, func, src in traceback.extract_tb(err[2]):
            ts_text = ts_text + \
            'File: %s, line %s, in %s\n\t%s\n'%(str(filename), str(line), str(func), str(src))

        traceback_stack = '\n' + ts_text + err_type.__name__ + ': ' + str(err_value) + '\n'
        logger_error.error(traceback_stack)

if __name__ == '__main__':
    #
    # module test
    #
    @record()
    def test(ain, bin1, cin):
        '''test function'''
        print ain, bin1, cin

    test('1', bin1='b', cin='3')

    @record(module='test2', description='test321')
    def error_test():
        '''error log test function'''
        open('123.txt', 'r')

    error_test()
