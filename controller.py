#!/usr/bin/env python

import tornado.web
import os
import subprocess
import time

FILE_DIR = 'files'
TASK_DIR = 'tasks'
RESULT_DIR = 'results'
PORT = 8888
IP = '127.0.0.1'

class upload_file(tornado.web.RequestHandler):
    def post(self, filename):
        print 'upload_file: ' + filename
        FILENAME = FILE_DIR + '/' + filename
        with open(FILENAME, 'wb') as f:
            f.write(self.request.body)
        self.set_status(200, 'OK')
        print 'file: ' + filename + ' uploaded'    

class upload_task(tornado.web.RequestHandler):
    def post(self, taskname):
        print 'upload_task: ' + taskname
        TASKNAME = TASK_DIR + '/' + taskname
        with open(TASKNAME, 'wb') as t:
            t.write(self.request.body)
        os.chmod(TASKNAME, 0755)
        print 'task ' + taskname + ' uploaded'

class run_task(tornado.web.RequestHandler):
    def get(self, taskname):
        print 'run_task: ' + taskname
        t = taskname.split('=')[0]
        f = taskname.split('=')[1]
        sb = subprocess.call([TASK_DIR + '/' + t, FILE_DIR + '/' + f, RESULT_DIR + '/' + t + '_' + time.strftime("%Y%m%d-%H%M%S")])
        print 'task: ' + taskname + ' ended'

if __name__ == '__main__':
    print 'starting'
    tornado_app = tornado.web.Application([(r'/upload_file/(.*)', upload_file),(r'/upload_task/(.*)', upload_task),(r'/run_task/(.*)', run_task)])
    tornado_app.listen(PORT, IP)
    tornado.ioloop.IOLoop.instance().start()
