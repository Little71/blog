import tornado.web
import tornado.ioloop
import tornado.websocket


class IndexHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


users = set()


class ChatHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        print('来人了')
        users.add(self)

    def on_message(self, message):
        content = self.render_string('message.html', msg=message)
        for client in users:
            client.write_message(content)

    def on_close(self):

        """
        客户端主动关闭连接
        :return:
        """
        users.remove(self)


def run():
    settings = {
        'template_path': 'templates',
        'static_path': 'static',
    }
    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat", ChatHandler),
    ], **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    run()
