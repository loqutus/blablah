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
PORT = 8885
IP = '127.0.0.1'
LOG_DIR = 'logs'
TIMEOUT = 10
CONTROLLER = '127.0.0.1:8888'


class upload_file(tornado.web.RequestHandler):
    def post(self, filename):
        debug('upload_file: ' + filename)
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
        debug('Running task: ' + TASK_DIR + '/' + t + ' ' + FILE_DIR + '/' + f + ' ' + RESULT_DIR + '/' + r)
        try:
            debug(subprocess.check_output(
                ['./' + TASK_DIR + '/' + t, './' + FILE_DIR +
                 '/' + f, './' + RESULT_DIR + '/' + r]))
        except subprocess.CalledProcessError, e:
            debug("task stdout output:\n", e.output)
        debug('task: ' + uri + ' ended')


class stop(tornado.web.RequestHandler):
    def get(self):
        debug('---stopping slave---')
        tornado.ioloop.IOLoop.instance().stop()


class get_result(tornado.web.RequestHandler):
    def get(self, resultname):
        debug('sending result: ' + resultname)
        with open(RESULT_DIR + '/' + resultname) as f:
            self.write(f.read())
        debug ('result sended successfully')

if __name__ == '__main__':
    if len(sys.argv)> 3:
        IP = sys.argv[1]
        PORT = sys.argv[2]
        CONTROLLER = sys.argv[3]
        FILE_DIR = FILE_DIR + '.' + PORT
        TASK_DIR = TASK_DIR + '.' + PORT
        RESULT_DIR = RESULT_DIR + '.' + PORT
    elif len(sys.argv) > 2:
        IP = sys.argv[1]
        PORT = sys.argv[2]
        FILE_DIR = FILE_DIR + '.' + PORT
        TASK_DIR = TASK_DIR + '.' + PORT
        RESULT_DIR = RESULT_DIR + '.' + PORT
    elif len(sys.argv) > 1:
        PORT = sys.argv[1]
        FILE_DIR = FILE_DIR + '.' + PORT
        TASK_DIR = TASK_DIR + '.' + PORT
        RESULT_DIR = RESULT_DIR + '.' + PORT
    else:
        pass
    logging.basicConfig(filename=LOG_DIR + '/' + 'slave' + str(PORT) + '.log',
                        format=u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)
    log = logging.getLogger(__name__)
    debug('---starting slave ---' + IP + ':' + str(PORT))
    debug('IP: ' + IP)
    debug('PORT: ' + str(PORT))
    debug('FILE_DIR: ' + FILE_DIR)
    debug('TASK_DIR: ' + TASK_DIR)
    debug('RESULT_DIR: ' + RESULT_DIR)
    debug('LOG_DIR: ' + LOG_DIR)
    debug('TIMEOUT: ' + str(TIMEOUT))
    tornado_app = tornado.web.Application(
        [(r'/upload_file/(.*)', upload_file), (r'/upload_task/(.*)',
        upload_task), (r'/run_task/(.*)', run_task), (r'/stop/', stop)
        ,(r'/get_result/(.*)', get_result)])
    tornado_app.listen(PORT, IP)
    tornado.ioloop.IOLoop.instance().start()
