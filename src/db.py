# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

from pymongo import MongoClient

from data import fake


class Db(object):
    def __init__(self, client=MongoClient, address=None, port=None):
        self.address = address or 'mongodb'#'127.0.0.1'
        self.port = port or 27017
        self.client = client

    def connect(self):
        return self.client(self.address, self.port)


if __name__ == "__main__":
    client = Db().connect()

    db = client.chat

    message_id = db.messages.insert_one(fake.message).inserted_id

    # db.messages.delete_many({})
    print(message_id)
