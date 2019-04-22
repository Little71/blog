import tornado.ioloop
import tornado.web

#同步阻塞
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        import time
        time.sleep(10)
        self.write("main")

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

















