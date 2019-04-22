import tornado.web
import tornado.websocket
import tornado.ioloop


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


users = set()


class ChatHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        print('有人来了...')
        users.add(self)

    def on_message(self, message):
        msg = self.render_string('message.html', msg=message)
        print(msg)
        for client in users:
            client.write_message(msg)

    def on_close(self):
        users.remove(self)


def run():
    settings = {
        'template_path': 'templates',
        'static_path': 'static'
    }
    application = tornado.web.Application([
        ('/', IndexHandler),
         ('/chat', ChatHandler)
    ],**settings)

    application.listen(8888)
    tornado.ioloop.IOLoop().instance().start()


if __name__ == '__main__':
    run()
