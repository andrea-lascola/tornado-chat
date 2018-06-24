# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

import json
from functools import partial

import pymongo
import tornado.ioloop
import time
import tornado.websocket
from toredis import Client as ToRedisClient

from entities import Message, Access
from utils import format_entity


class WebSocket(tornado.websocket.WebSocketHandler):

    user = None
    channel = None

    def open(self):
        # Get user and channel
        self.user = self.get_argument('user', None)
        self.channel = self.get_argument('channel', None)

        #print("WebSocket opened by {}, channel={}".format(self.user,self.channel))

        messages = self.application.db.messages.find({"channel" : self.channel}).sort("$natural",pymongo.DESCENDING).limit(5)

        output = [format_entity(msg) for msg in messages]

        for message in reversed(output):
            self.write_message(message)

        self.application.manager.register(self.user,self.channel,self)

    def on_message(self, message):
        entity = Message.from_dict(json.loads(message))
        self.application.db.messages.insert_one(entity.__dict__)
        self.application.manager.notify(entity.channel,format_entity(entity.__dict__))

    def on_close(self):
        # print("WebSocket closed")
        self.application.manager.unregister(self.user,self.channel)

class RedisWebSocket(tornado.websocket.WebSocketHandler):

    client = None
    user = None
    channel = None
    io_loop = tornado.ioloop.IOLoop.instance()

    def open(self):
        # Get user and channel
        self.user = self.get_argument('user', None)
        self.channel = self.get_argument('channel', None)

        # new access
        self.application.db.access.insert_one(Access.connect(self.user,self.channel).__dict__)

        # get all messages
        messages = self.application.db.messages.find({"channel" : self.channel}).sort("$natural",pymongo.DESCENDING)

        output = [format_entity(msg) for msg in messages]

        for message in reversed(output):
            self.write_message(message)

        # subscribe to channel
        self.client = ToRedisClient()
        self.client.connect(host="redis")
        self.client.subscribe(self.channel, callback=self.on_receive)

    def on_receive(self,msg):
        msg_type, msg_channel, msg = msg
        if msg_type == b"message":
            self.write_message(eval(msg))
        # client.write_message(message)

    def on_message(self, message):
        entity = Message.from_dict(json.loads(message))
        self.application.db.messages.insert_one(entity.__dict__)

        conn = ToRedisClient()
        conn.connect(host="redis")

        def publish_message(channel,message):
            conn.publish(channel,message)

        self.io_loop.add_timeout(time.time(), partial(publish_message,self.channel,format_entity(entity.__dict__)))
        # self.application.manager.notify(entity.channel,format_entity(entity.__dict__))

    def on_close(self):
        self.application.db.access.insert_one(Access.disconnect(self.user, self.channel).__dict__)
        self.client.unsubscribe(self.channel)
        # print("WebSocket closed")
        # self.application.manager.unregister(self.user,self.channel)

