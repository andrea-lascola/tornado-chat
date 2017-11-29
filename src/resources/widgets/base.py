# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

import abc
import uuid


class Widget(object):
    __metaclass__ = abc.ABCMeta

    default_options = dict(
        title="My Widget"
    )

    def __init__(self, data):
        self._data = data

    @abc.abstractmethod
    def render(self, options):
        pass

    def get_opt(self,options,prop):
        """
        Return the property from option dict -> fallback on defaults
        :param options: options dict
        :param prop:prop
        :return: value
        """
        if isinstance(options,dict):
            return options.get(prop,self.default_options.get(prop))
        return self.default_options.get(prop)

def widget_id():
    return str(uuid.uuid4())
