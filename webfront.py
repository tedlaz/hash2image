#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

# Find details about this project at https://github.com/e1ven/robohash

from tornado.options import define, options
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import socket
import os
import hashlib
import random
import re
import io
import urllib.request
import urllib.parse
from hash2image import create_image


urlopen = urllib.request.urlopen
urlencode = urllib.parse.urlencode
define("port", default=8099, help="run on the given port", type=int)
DEFAULT_SET = 'coats'


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello there')


class ImgHandler(tornado.web.RequestHandler):
    def get(self, string=None):
        string = '' if string is None else string
        valid_sets = ['cats', 'coats', 'monsters', 'people', 'robotfaces', 'robots']
        sizexy = 300
        rset = ''
        args = self.request.arguments.copy()
        if 'size' in args:
            sizexy = int(args['size'][0].decode())
            if sizexy > 4096:
                sizexy = 1024
            elif sizexy < 0:
                sizexy = 300
        if 'set' in args:
            rset = args['set'][0].decode()
        if rset not in valid_sets:
            rset = DEFAULT_SET
        self.set_header("Content-Type", "image/png")
        self.set_header("Cache-Control", "public,max-age=31536000")
        image, fingerprint = create_image(string, sizexy, rset=rset)
        image.save(self, format='png')


def main():
    tornado.options.parse_command_line()
    timeout = 10
    socket.setdefaulttimeout(timeout)
    settings = {
        "cookie_secret": "12ab34ff4566800012211234567890fd",
        "xsrf_cookies": True,
    }
    application = tornado.web.Application([
        (r"/", ImgHandler),
        (r"/(.*)", ImgHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)
    print(f'hash2image webfront is listening on port: {str(options.port)}')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
