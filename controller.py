#!/usr/bin/env python

import tornado.web
import ipdb

DIR = 'files'
PORT = 8888
IP = '127.0.0.1'

class Upload(tornado.web.RequestHandler):
    def post(self, filename):
        FILENAME = DIR + '/' + filename
        with open(FILENAME, 'wb') as f:
            f.write(self.request.body)
        self.set_status(200, 'OK')

if __name__ == '__main__':
    tornado_app = tornado.web.Application([(r'/upload/(.*)', Upload)])
    tornado_app.listen(PORT, IP)
    tornado.ioloop.IOLoop.instance().start()
