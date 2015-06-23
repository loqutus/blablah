#!/usr/bin/env python

import sys
import requests

TIMEOUT = 10


def upload_file(controller, filename):
    print 'uploading file: ' + filename + ' to ' + controller
    url_upload = 'http://' + controller + '/upload_file/' + filename
    with open(filename, 'rb') as f:
        requests.post(url_upload, f.read(), timeout=TIMEOUT)
    print 'file uploaded !'


def upload_task(controller, taskname):
    print 'uploading task: ' + taskname + ' to ' + controller
    url_upload = 'http://' + controller + '/upload_task/' + taskname
    with open(taskname, 'rb') as f:
        requests.post(url_upload, f.read(), timeout=TIMEOUT)
    print 'uploaded !'


def run_task(controller, task):
    url_run = 'http://' + controller + '/run_task/' + task
    print 'running task: ' + url_run
    requests.get(url_run, timeout=TIMEOUT)
    print 'task runned!'


def stop(url_stop):
    print 'stopping: ' + url_stop
    requests.get(url_stop, timeout=TIMEOUT)
    print 'stopped!'


def register_task(controller, task, filename):
    print 'register_task: ' + task + ' ' + filename
    url = 'http://' + controller + '/register_task/' + task + '=' + filename
    requests.get(url, timeout=TIMEOUT)
    debug('task registered!')


if __name__ == '__main__':
    ACTION = sys.argv[1]
    CONTROLLER = sys.argv[2]
    if ACTION == 'upload_file':
        FILENAME = sys.argv[3].split("/")[-1]
        upload_file(CONTROLLER, FILENAME)
    elif ACTION == 'upload_task':
        TASKNAME = sys.argv[3].split("/")[-1]
        upload_task(CONTROLLER, TASKNAME)
    elif ACTION == 'run_task':
        TASKNAME = sys.argv[3]
        FILENAME = sys.argv[4]
        RESULTNAME = sys.argv[5]
        TASK = TASKNAME + '=' + FILENAME + '=' + RESULTNAME
        run_task(CONTROLLER, TASK)
    elif ACTION == 'stop_controller':
        URL_STOP = 'http://' + CONTROLLER + '/stop/'
        stop(URL_STOP)
    elif ACTION == 'stop_slave':
        SLAVE = sys.argv[2]
        URL_STOP = 'http://' + SLAVE + '/stop/'
        stop(URL_STOP)
    elif ACTION == 'register_task':
        CONTOLLER = sys.argv[2]
        TASK = sys.argv[3]
        FILENAME = sys.argv[4]
        register_task(CONTROLLER, TASK, FILENAME)
