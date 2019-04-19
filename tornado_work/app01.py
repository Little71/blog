import datetime
import hashlib

import tornado.web
import tornado.ioloop

import uimethods as mt
import uimodules as ml
from controllers.account import LoginHandler
from controllers.home import HomeHandler


class Cache:
    def __init__(self):
        self.container = {}

    def __contains__(self, item):
        return item in self.container

    def inition(self,random_str):
        self.container[random_str] = {}

    def get(self,random_str, item):
        return self.container[random_str].get(item)

    def set(self,random_str, key, value):
        self.container[random_str][key] = value

    def delete(self,random_str, item):
        del self.container[random_str][item]

    def clear(self,random_str):
        del self.container[random_str]

    def open(self):
        pass

    def close(self):
        pass



p = Cache

# container = {'xxx':{}}
class Session:
    def __init__(self,handler):
        self.handler = handler
        self.random_str = None
        self.db = p()

        client_random_str = self.handler.get_cookie('session_id')
        if not client_random_str:
            self.random_str = self.create_random_str()
            self.db.inition(self.random_str)
        else:
            if client_random_str in container:
                self.random_str = client_random_str
            else:
                self.random_str = self.create_random_str()

        self.handler.set_cookie('session_id', self.random_str)

    def create_random_str(self):
        import os
        return os.urandom(24)

    def __setitem__(self, key, value):
        self.db.set(self.random_str,key,value)

    def __getitem__(self, item):
        return self.db.get(self.random_str,item)

    def __delitem__(self, key):
        self.db.delete(self.random_str,key)

    def clear(self):
        self.db.clear(self.random_str)


class FooMixin:
    def initialize(self):
        #定制钩子
        self.A = 123
        self.session = Session(self)
        super().initialize()


class MainHandler(FooMixin,tornado.web.RequestHandler):

    def get(self):
        self.write(f'{self.A}')
        self.request.session['is_login'] = True
        self.request.session['is_login'] = True


application = tornado.web.Application([
    ('/index', MainHandler),
])

if __name__ == '__main__':
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
