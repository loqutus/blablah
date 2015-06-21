#!/usr/bin/env python

import sys
import requests

HOST = '127.0.0.1'
PORT = '8888'
TIMEOUT = 10
URL = 'http://' + HOST + ':' + PORT

def upload_file(filename, url_upload):
    print 'uploading file: ' + filename + ' to ' + url_upload
    with open(filename, 'rb') as f:
        requests.post(url_upload, f.read(), timeout = TIMEOUT)
    print 'uploaded !'

def upload_task(taskname, url_upload):
    print 'uploading task: ' + taskname + ' to ' + url_upload
    with open(taskname, 'rb') as f:
        requests.post(url_upload, f.read(), timeout = TIMEOUT)
    print 'uploaded !'

def run_task(url_run):
    print 'running task: ' + url_run
    requests.get(url_run, timeout = TIMEOUT)
    print 'task runned!'
    
def stop(url_stop):
    print 'stopping: ' + url_stop
    requests.get(url_stop, timeout = TIMEOUT)
    print 'stopped!'

if __name__ == '__main__':
    ACTION = sys.argv[1]
    if ACTION == 'upload_file':
        FILENAME = sys.argv[2].split("/")[-1]
        URL_UPLOAD = URL + '/upload_file/' + FILENAME
        upload_file(FILENAME, URL_UPLOAD)
    elif ACTION == 'upload_task':
        TASKNAME = sys.argv[2].split("/")[-1]
        URL_UPLOAD = URL + '/upload_task/' + TASKNAME
        upload_task(TASKNAME, URL_UPLOAD)
    elif ACTION == 'run_task':
        TASKNAME = sys.argv[2]
        FILENAME = sys.argv[3]
        RESULTNAME = sys.argv[4]
        URL_RUN = URL + '/run_task/' + TASKNAME + '=' + FILENAME + '=' + RESULTNAME
        run_task(URL_RUN)
    elif ACTION == 'stop_controller':
        CONTROLLER = sys.argv[2]
        URL_STOP = 'http://' + CONTROLLER + '/stop/'
        stop(URL_STOP)
    elif ACTION == 'stop_slave':
        SLAVE = sys.argv[2]
        URL_STOP = 'http://' + SLAVE + '/stop/'
        stop(URL_STOP)
