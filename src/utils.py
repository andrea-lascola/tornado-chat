# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals
import datetime


def ellipsize(message, limit=100):
    return "{}...".format(message[:limit]) if len(message) > limit else message


def format_entity(entity):
    for k, v in entity.items():
        if isinstance(v, datetime.date):
            entity[k] = str(v)

    del entity["_id"]
    return entity

def pipe(data,functions):
    result = data
    for function in functions:
        result = function(result)
    return result
