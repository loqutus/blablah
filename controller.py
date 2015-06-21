#!/usr/bin/env python

import sys
import requests
import tornado.web
import subprocess
import itertools
import logging
import ipdb
from logging import debug

IP = '127.0.0.1'
PORT = '8888'
TIMEOUT = 10
HOSTS = 'hosts'
SPLIT_DIR = 'splits'
FILE_DIR = 'files'
TASK_DIR = 'tasks'
RESULT_DIR = 'results'
LOG_DIR = 'logs'

logging.basicConfig(filename = LOG_DIR + '/' + 'controller.log', format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)
log = logging.getLogger(__name__)

def split(filename):
    debug('slicing start')
    splits_list = []
    count_lines = 0
    count_hosts = 0
    split_path = SPLIT_DIR + '/' + filename
    file_path = FILE_DIR + '/' + filename
    with open(HOSTS, 'r') as h:
        for i in h:
            count_hosts += 1
    debug('count_hosts: '+ str(count_hosts))    
    with open(file_path, 'r') as f:
        for i in f:
            count_lines += 1
    debug('count_lines: ' + str(count_lines))
    lines_per_split = count_lines / count_hosts
    debug('lines_per_split: ' + str(lines_per_split))
    i = 0
    with open(file_path, 'rb') as g:
        while i < count_hosts: 
            debug('splitting: ' + str(i))
            splits_list.append(filename + '.' + str(i))
            split_name = split_path + '.' + str(i)
            with open(split_name, 'wb') as f:
                j = 0
                debug('open: ' + split_path + '.' + str(i))
                while j < lines_per_split:
                    f.write(g.next())
                    j += 1    
                debug('close: ' + split_path + '.' + str(i))
            i += 1
    return splits_list
    
class upload_file(tornado.web.RequestHandler):
    def post(self, filename):
        debug('saving: ' + filename)
        path = FILE_DIR + '/' + filename
        with open(path, 'wb') as f:
            f.write(self.request.body)
        debug('saved: ' + filename)        
        split_files = split(filename)        
        with open(HOSTS, 'r') as f:
            split_hosts = f.readlines()
        for i in range(0,len(split_hosts)):
            line = split_hosts[i]
            split_upload = split_files[i]
            host = line.split(' ')[0]
            port = line.split(' ')[1][:-1]
            url_upload = 'http://' + host + ':' + port + '/upload_file/' +split_upload 
            debug('uploading file: ' + split_upload + ' to ' + url_upload)
            with open(SPLIT_DIR + '/' + split_upload, 'rb') as f:
                requests.post(url_upload, f.read(), timeout = TIMEOUT) 
                debug('uploaded: ' + url_upload)
        self.set_status(200, 'OK')
        debug('file uploading finished!')

class stop(tornado.web.RequestHandler):
    def get(self):
        debug('---stopping controller---')
        self.set_status(200, 'OK')
        tornado.ioloop.IOLoop.instance().stop()

class upload_task(tornado.web.RequestHandler):
    def post(self, filename):
        debug('uploading task')
        task_path = TASK_DIR + '/' + filename
        with open(task_path, 'wb') as f:
            f.write(self.request.body)
            debug('task ' + filename + ' saved')
        with open(HOSTS, 'r') as h:
            host_lines = h.readlines()
            for line in host_lines:
                host = line.split(' ')[0]
                port = line.split(' ')[1][:-1]
                url_upload = 'http://' + host + ':' + port + '/upload_task/' + filename 
                debug(url_upload)
                debug('uploading task ' + filename + ' to ' + url_upload)
                with open(task_path, 'rb') as f:
                    requests.post(url_upload, f.read(), timeout = TIMEOUT)
                debug('task ' + filename + ' uploaded')
        self.set_status(200, 'OK')
        debug('task uploading finished')            

class run_task(tornado.web.RequestHandler):
    def get(self, taskname):
        debug('running task: ' + taskname)
        with open(HOSTS, 'r') as h:
            host_lines = h.readlines()
            for line in host_lines:
                host = line.split(' ')[0]
                port = line.split(' ')[1][:-1]
                url_run = 'http://' + host + ':' + port + '/run_task/' + taskname
                debug('running task: ' + url_run)
                requests.get(url_run, timeout = TIMEOUT)
                debug('task ' + taskname + ' runned on  ' + url_run)
        debug('task runned on all slaves!')
        self.set_status(200, 'OK')
    
if __name__ == '__main__':
    debug('---starting controller---')
    tornado_app = tornado.web.Application([(r'/upload_file/(.*)', upload_file),(r'/upload_task/(.*)', upload_task),(r'/run_task/(.*)', run_task),(r'/stop/', stop)])
    tornado_app.listen(PORT, IP)
    debug('IP: ' + IP)
    debug('PORT: ' + PORT)
    debug('TIMEOUT: ' + str(TIMEOUT))
    debug('HOSTS: ' + HOSTS)
    debug('FILE_DIR: ' + FILE_DIR)
    debug('SPLIT_DIR: ' + SPLIT_DIR)
    debug('TASK_DIR: ' + TASK_DIR)
    debug('RESULT_DIR: ' + RESULT_DIR)
    debug('LOG_DIR: ' + LOG_DIR)
    tornado.ioloop.IOLoop.instance().start()
