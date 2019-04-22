import socket
import select


class HttpRequest(object):
    """
    用户封装用户请求信息
    """

    def __init__(self, content):
        '''

        :param content: 用户请求参数
        '''
        self.content = content

        self.header_bytes = bytes()
        self.header_dict = {}
        self.body_bytes = bytes()

        self.method = ""
        self.url = ""
        self.protocol = ""

        self.initialize()
        self.initialize_headers()

    def initialize(self):

        temp = self.content.split(b'\r\n\r\n', 1)
        if len(temp) == 1:
            self.header_bytes += temp
        else:
            h, b = temp
            self.header_bytes += h
            self.body_bytes += b

    @property
    def header_str(self):
        return str(self.header_bytes, encoding='utf-8')

    def initialize_headers(self):
        headers = self.header_str.split('\r\n')
        first_line = headers[0].split(' ')
        if len(first_line) == 3:
            self.method, self.url, self.protocol = headers[0].split(' ')
            for line in headers:
                kv = line.split(':')
                if len(kv) == 2:
                    k, v = kv
                    self.header_dict[k] = v


def main(request):
    return 'main'


def index(request):
    return 'index'


routes = [
    ('/main', main),
    ('/index', index),
]


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 9999,))
    sock.setblocking(False)
    sock.listen(128)
    sock.setblocking(0)

    inputs = []
    inputs.append(sock)
    while True:
        rlist, wlist, elist = select.select(inputs, [], [], 0.05)
        for r in rlist:
            if r == sock:
                '''新请求到来'''
                conn, addr = sock.accept()
                conn.setblocking(0)
                inputs.append(conn)
            else:
                '''客户端发来请求数据'''
                data = bytes()
                while True:
                    try:
                        chunk = r.recv(1024)
                        data += chunk
                    except Exception as e:
                        chunk = None
                    if not chunk:
                        break

                '''
                1、请求头获取url，去路由匹配
                2、匹配成功执行对应的函数
                3、获取函数返回值，send回去
                '''
                request = HttpRequest(data)
                import re
                flag = False
                func = None
                for route in routes:
                    if re.match(route[0], request.method):
                        flag = True
                        func = route[1]
                        break
                if flag:
                    response = func(request)
                    r.sendall(bytes(response, encoding='utf-8'))
                else:
                    r.sendall(b'404')
                r.close()
                inputs.remove(r)

if __name__ == '__main__':
    run()