# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

import os
import uuid

import motor
import pymongo
import redis
import tornado.websocket
import tornado.ioloop
import tornado.web
from collections import defaultdict

from db import Db
from tornado.options import define, options

from resources import dashboard
from resources import messages
from resources import socket
from resources.login import LoginHandler

define("port", default=8887, help="Http Port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "key",# dunno if i have to generate a random or use a key. str(uuid.uuid4()),
        "login_url": "/login",
        # "xsrf_cookies": True,
    }
    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/messages", messages.MessagesHandler),
        (r"/async_messages", messages.AsyncMessagesHandler),
        (r"/ws", socket.RedisWebSocket),
        (r"/dashboard", dashboard.DashBoardHome),

        (r"/login", LoginHandler),

        (r"/images/(.*)", tornado.web.StaticFileHandler, {'path': "./static/images"}),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {'path': "./static/css"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {'path': "./static/js"}),
        # (r"/login", LoginHandler),
        # (r"/(apple-touch-icon\.png)",
        # tornado.web.StaticFileHandler,
        #  dict(path=settings['static_path']),
    ], **settings)

    application.db = Db(pymongo.MongoClient).connect().chat
    application.asyncdb = Db(motor.motor_tornado.MotorClient).connect().chat

    # application.asyncdb = motor.motor_tornado.MotorClient('localhost', 27017).chat

    return application


if __name__ == "__main__":
    app = make_app()
    options.parse_command_line()

    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


