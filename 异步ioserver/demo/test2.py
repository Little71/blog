import tornado.ioloop
import tornado.web

from tornado import gen
from tornado.concurrent import Future


# 异步非阻塞
class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        import time
        future = Future()
        # 5秒后执行done
        tornado.ioloop.IOLoop.current().add_timeout(time.time() + 5, self.done)
        yield future

    def done(self, *args, **kwargs):
        self.write('main')
        self.finish()


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("index")


application = tornado.web.Application([
    (r"/main", MainHandler),
    (r"/index", IndexHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
