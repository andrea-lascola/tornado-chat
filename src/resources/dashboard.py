# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals

import json

import tornado.web
import plotly

from data import dataproviders
from resources.widgets import components


class DashBoardHome(tornado.web.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        user = tornado.escape.xhtml_escape(self.current_user)

        graphs = [
            [
                components.Pie(
                    dataproviders.channels_messages(self.application.db)
                ).render(options=dict(
                    title="Most active channels"
                )),
                components.Bar(
                    dataproviders.most_active_users(self.application.db)
                ).render(options=dict(
                    title="Most Active Users"
                )),
                components.Bar(
                    dataproviders.most_frequest_words(self.application.db)
                ).render(options=dict(
                    title="Most Frequent Words"
                ))
            ], [
                components.Line(
                    dataproviders.messages_per_hours(self.application.db)
                ).render(options=dict(
                    title="Messages during the day"
                )),
            ]
        ]

        graph_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        self.render('dashboard.html',
                    user=user,
                    graphJSON=graph_json,
                    graphs=graphs,
                    )

    def get_current_user(self):
        return self.get_secure_cookie("user")
