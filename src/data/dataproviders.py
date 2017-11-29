# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

import functools
import operator

from bson import SON

from utils import pipe


def dataprovider(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        data = func(*args, **kwargs)

        if not isinstance(data, BaseData):
            raise ValueError("Invalid Dataprovider in {}".format(func.__name__))

        return data

    return inner


class BaseData(object):
    pass


class ChartData(BaseData):
    _xaxis = None
    _yaxis = None

    def __init__(self, xaxis=None, yaxis=None):
        self._xaxis = xaxis
        self._yaxis = yaxis

    @property
    def xaxis(self):
        return self._xaxis

    @property
    def yaxis(self):
        return self._yaxis


class GridData(BaseData):
    _rows = None

    def __init__(self, rows):
        self._rows = rows

    @property
    def rows(self):
        return self._rows


@dataprovider
def most_active_users(db, channel=None):
    """
    Aggregate and groupby channel
    :param db: database connection
    :return: ChartData
    """
    pipeline = [
        {"$unwind": "$user"},
        {"$group": {"_id": "$user", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1)])}
    ]

    data = list(db.messages.aggregate(pipeline))

    return ChartData(map(operator.itemgetter('_id'), data),
                     map(operator.itemgetter('count'), data))


@dataprovider
def channels_messages(db):
    """
    Aggregate and groupby channel
    :param db: database connection
    :return: ChartData
    """
    pipeline = [
        {"$unwind": "$channel"},
        {"$group": {"_id": "$channel", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1)])}
    ]

    data = list(db.messages.aggregate(pipeline))

    return ChartData(map(operator.itemgetter('_id'), data),
                     map(operator.itemgetter('count'), data))


@dataprovider
def most_frequest_words(db, pypipeline=None):
    """
    Most frequent words in messages
    :param db:
    :param pypipeline: optional filter functions
    :return: ChartData
    """

    def limit(n):
        def inner(data):
            return data[:n]

        return inner

    def filter_short_word(n):
        def inner(data):
            return filter(lambda x: len(x.get('_id')) > n, data)

        return inner

    pypipeline = pypipeline or [
        filter_short_word(3),
        limit(10)
    ]
    pipeline = [
        # {"$unwind": "$user"},
        {"$project": {"word": {"$split": ["$message", " "]}}},
        {"$unwind": "$word"},
        {"$group": {"_id": "$word", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1)])}
    ]

    data = pipe(list(db.messages.aggregate(pipeline)), pypipeline)
    return ChartData(map(operator.itemgetter('_id'), data),
                     map(operator.itemgetter('count'), data))


@dataprovider
def messages_per_hours(db):
    """
    Number of messages per hour of the day
    :param db: database connection
    :return:
    """
    pipeline = [
        {"$project": {
            "hour": {"$hour": "$date"}
        }},
        {"$unwind": "$hour"},
        {"$group": {"_id": "$hour", "count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])}
    ]

    data = list(db.messages.aggregate(pipeline))
    return ChartData(map(operator.itemgetter('_id'), data),
                     map(operator.itemgetter('count'), data))


@dataprovider
def last_n_messages(db, n=5):
    """

    :param db:
    :param n:
    :return:
    """
    messages = db.messages.find().sort([("date", -1)]).limit(n)
    return GridData([dict(user=message.get("user"),
                          channel=message.get("channel"),
                          message=message.get("message"),
                          date=message.get("date")) for message in messages])
