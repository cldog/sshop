#coding=utf-8
from sshop.base import BaseHandler


class NotFoundHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.render('404.html')
