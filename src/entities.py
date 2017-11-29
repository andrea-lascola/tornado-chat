# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals
import datetime

from utils import ellipsize


class Message(object):
    message = None
    date = None
    user = None
    channel = None

    def __init__(self, message, date, user, channel):
        self.date = date
        self.message = message
        self.user = user
        self.channel = channel

    @classmethod
    def from_dict(cls, message):
        return cls(message=message.get("message"),
                   user=message.get("user"),
                   channel=message.get("channel"),
                   date=datetime.datetime.now())

    def __repr__(self):
        return "<Message user={}, date={}, channel={}, message={}>".format(self.user, self.date, self.channel,
                                                                           ellipsize(self.message))

    def __str__(self):
        return self.__repr__()


class AccessType(object):
    CONNECT = "connect"
    DISCONNECT = "disconnect"

class Access(object):
    user = None
    date = None
    access_type = None
    channel = None

    def __init__(self, user, date, access_type, channel):
        self.user = user
        self.date = date
        self.access_type = access_type
        self.channel = channel

    @classmethod
    def connect(cls,user,channel):
        return cls(
            user=user,
            channel=channel,
            date=datetime.datetime.now(),
            access_type=AccessType.CONNECT
        )

    @classmethod
    def disconnect(cls,user,channel):
        return cls(
            user=user,
            channel=channel,
            date=datetime.datetime.now(),
            access_type=AccessType.DISCONNECT
        )

    def __repr__(self):
        return "<Access user={}, date={}, channel={}, access_type={}>".format(self.user, self.date, self.channel,self.access_type)

    def __str__(self):
        return self.__repr__()