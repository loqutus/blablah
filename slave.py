#!/usr/bin/env python

import tornado.web
import os
import subprocess
import time
import sys
import logging
from logging import debug

FILE_DIR = 'files'
TASK_DIR = 'tasks'
RESULT_DIR = 'results'
PORT = 8888
IP = '127.0.0.1'

class upload_file(tornado.web.RequestHandler):
    def post(self, filename):
        debug ('upload_file: ' + filename)
        FILENAME = FILE_DIR + '/' + filename
        with open(FILENAME, 'wb') as f:
            f.write(self.request.body)
        self.set_status(200, 'OK')
        debug('file: ' + filename + ' uploaded')

class upload_task(tornado.web.RequestHandler):
    def post(self, taskname):
        debug('upload_task: ' + taskname)
        TASKNAME = TASK_DIR + '/' + taskname
        with open(TASKNAME, 'wb') as t:
            t.write(self.request.body)
        os.chmod(TASKNAME, 0755)
        debug('task ' + taskname + ' uploaded')

class run_task(tornado.web.RequestHandler):
    def get(self, uri):
        debug('run_task: ' + uri)
        t = uri.split('=')[0]
        f = uri.split('=')[1]
        r = uri.split('=')[2]
        sb = subprocess.call([TASK_DIR + '/' + t, FILE_DIR + '/' + f, RESULT_DIR + '/' + r)]
        debug('task: ' + taskname + ' ended')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    elif len(sys.argv) > 2:
        IP = sys.argv[1]
        PORT = sys.argv[2]
    else:
        pass
    logging.basicConfig(filename='slave' + PORT + '.log', format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)
    debug('starting slave')
    tornado_app = tornado.web.Application([(r'/upload_file/(.*)', upload_file),(r'/upload_task/(.*)', upload_task),(r'/run_task/(.*)', run_task)])
    tornado_app.listen(PORT, IP)
    tornado.ioloop.IOLoop.instance().start()
