# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

from resources.widgets.base import Widget, widget_id

"""

Pie - % messages in channels

Bar / Grid - Most active users



Bar - Most frequent words

Linechart - access during days


"""

class Scatter(Widget):
    def render(self, options):
        return dict(
            id=widget_id(),
            data=[
                dict(
                    x=self._data.xaxis,
                    y=self._data.yaxis,
                    type='markers'
                ),
            ],
            layout=dict(
                title=self.get_opt(options,'title')
            )
        )


class Pie(Widget):
    def render(self, options):
        return dict(
            id=widget_id(),
            data=[
                dict(
                    labels=self._data.xaxis,
                    values=self._data.yaxis,
                    type='pie'
                ),
            ],
            layout=dict(
                title=self.get_opt(options,'title')
            )
        )


class Bar(Widget):
    def render(self, options):
        return dict(
            id=widget_id(),
            data=[
                dict(
                    x=self._data.xaxis,
                    y=self._data.yaxis,
                    type='bar'
                ),
            ],
            layout=dict(
                title=self.get_opt(options,'title')
            )
        )

class Line(Widget):
    def render(self, options):
        return dict(
            id=widget_id(),
            data=[
                dict(
                    x=self._data.xaxis,
                    y=self._data.yaxis,
                    type='lines'
                ),
            ],
            layout=dict(
                title=self.get_opt(options,'title')
            )
        )
class Grid(Widget):
    def render(self, options):

        return self._data.rows()

        # return dict(
        #     id=widget_id(),
        #     data=[
        #         dict(
        #             x=self._data.xaxis,
        #             y=self._data.yaxis,
        #             type='lines'
        #         ),
        #     ],
        #     layout=dict(
        #         title=self.get_opt(options,'title')
        #     )
        # )