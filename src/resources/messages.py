# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

import tornado.web
from tornado import gen


class AsyncMessagesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        cursor = self.application.asyncdb.messages.find()

        msgs = []
        while (yield cursor.fetch_next):
            msg = cursor.next_object()
            msg["idate"] = str(msg["idate"])
            del msg["_id"]
            msgs.append(msg)

        self.write({"messages": msgs})


class MessagesHandler(tornado.web.RequestHandler):
    def get(self):
        messages = self.application.db.messages.find()

        msgs = []

        for msg in messages:
            msg["idate"] = str(msg["idate"])
            del msg["_id"]
            msgs.append(msg)

        self.write({"messages": msgs})
