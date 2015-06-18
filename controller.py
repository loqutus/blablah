#!/usr/bin/env python

import sys
import requests
import tornado.web
import subprocess
import itertools
import logging

IP = '127.0.0.1'
PORT = '8888'
TIMEOUT = 10
HOSTS = 'hosts'
SPLIT_DIR = 'splits'
FILE_DIR = 'files'
TASK_DIR = 'tasks'
RESULT_DIR = 'results'

logging.basicConfig(filename='controller.log', format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)
log = logging.getLogger(__name__)

def split(filename):
    log.debug('slicing start')
    count_lines = 0
    count_hosts = 0
    split_path = SPLIT_DIR + '/' + filename
    file_path = FILE_DIR + '/' + filename
    with open(HOSTS, 'r') as h:
        for i in h:
            count_hosts += 1
    log.debug('count_hosts: '+ str(count_hosts))    
    with open(file_path, 'r') as f:
        for i in f:
            count_lines += 1
    log.debug('count_lines: ' + str(count_lines))
    lines_per_split = count_lines / count_hosts
    log.debug('lines_per_split: ' + str(lines_per_split))
    i = 0
    with open(file_path, 'rb') as g:
        while i < count_hosts: 
            log.debug('splitting: ' + str(i))
            with open(split_path + '.' + str(i), 'wb') as f:
                j = 0
                log.debug('open: ' + split_path + '.' + str(i))
                while j < lines_per_split:
                    f.write(g.next())
                    j += 1    
                log.debug('close: ' + split_path + '.' + str(i))
            i += 1
    return 0

    
class upload_file(tornado.web.RequestHandler):
    def post(self, filename):
        log.debug('saving: ' + filename)
        path = FILE_DIR + '/' + filename
        with open(path, 'wb') as f:
            f.write(self.request.body)
        log.debug('saved: ' + filename)        
        split(filename)        
#        f = open(HOSTS, 'r')
        #for i in f:
        #       host = i.split(' ')[0]
#    port = i.split(' ')[1]
#            url_upload = 'http://' + host + ':' + port + '/upload_file/' + filename
#            log.debug('uploading file: ' + filename + ' to ' url_upload)
#            with open(path, 'rb') as f:
#                requests.post(url_upload, f.read(), timeout = TIMEOUT)
#        
#            log.debug(url_upload + 'uploaded !')
    log.debug('file uploading finished!')

def upload_task(taskname, url_upload):
    log.debug('uploading task: ' + taskname + ' to ' + url_upload)
#path = 
    with open(taskname, 'rb') as f:
        requests.post(url_upload, f.read(), timeout = TIMEOUT)
    log.debug('task uploaded !')

def run_task(url_run):
    log.debug('running task: ' + url_run)
    requests.get(url_run, timeout = TIMEOUT)
    log.debug('task runned!')
    
if __name__ == '__main__':
    log.debug('---starting controller---')
    tornado_app = tornado.web.Application([(r'/upload_file/(.*)', upload_file),(r'/upload_task/(.*)', upload_task),(r'/run_task/(.*)', run_task)])
    tornado_app.listen(PORT, IP)
    tornado.ioloop.IOLoop.instance().start()
