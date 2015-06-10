#!/usr/bin/env python

import sys
import requests
import ipdb

HOST = '127.0.0.1'
PORT = '8888'
TIMEOUT = 10
URL = 'http://' + HOST + ':' + PORT

def upload(filename):
    print 'uploading: ' + filename + ' to ' + URL_UPLOAD
    with open(filename, 'rb') as f:
        requests.post(URL_UPLOAD, f.read(), timeout = TIMEOUT)
    print 'uploaded !'

if __name__ == '__main__':
    ACTION = sys.argv[1]
    if ACTION == 'upload':
        FILENAME = sys.argv[2].split("/")[-1]
        URL_UPLOAD = URL + '/upload/' + FILENAME
        upload(FILENAME)
