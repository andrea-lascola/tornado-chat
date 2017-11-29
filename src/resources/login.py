# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division, unicode_literals


import tornado.web
# class LoginHandler(tornado.web.RequestHandler):
#     pass
from tornado import gen


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write('<html><body><form action="/login" method="post">'
        #            'Name: <input type="text" name="name">'
        #            '<input type="submit" value="Sign in">'
        #             '<input type="hidden" name="next" value="{}">'
        #            '</form></body></html>'.format(self.get_argument("next","/"))
        #            )

        self.render('login.html',next=self.get_argument("next","/"))



    @gen.coroutine
    def post(self):

        if self.get_argument("name") == "andrea":
            self.set_secure_cookie("user", self.get_argument("name"),expires_days=1)
        #self.redirect("/")
            self.redirect(self.get_argument("next", u"/"))
        else:
            self.redirect(u"/login?next="+self.get_argument("next"))
