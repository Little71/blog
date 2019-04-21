import socket
import select

class HttpResponse:
    def __init__(self, recv_data):
        self.recv_data = recv_data
        self.body = None
        self.header_dict = {}
        self.initialize()

    def initialize(self):
        header, body = self.recv_data.split(b'\r\n\r\n', 1)
        self.body = body
        head_list = str(header,encoding='utf-8').split('\r\n')
        for i in head_list:
            v = i.split(':',1)
            if len(v) == 2:
                self.header_dict[v[0]] = v[1]



class HttpRequest:
    def __init__(self, host, socket, callback):
        self.host = host
        self.socket = socket
        self.callback = callback

    def fileno(self):
        return self.socket.fileno()


class AsynicClient:
    def __init__(self):
        self.conn = []
        self.connection = []

    def add_request(self, host, callback):
        sk = socket.socket()
        sk.setblocking(0)
        try:
            sk.connect((host,80))
        except BlockingIOError as e:
            pass
        httprequest = HttpRequest(host, sk, callback)
        self.conn.append(httprequest)
        self.connection.append(httprequest)

    def run(self):
        while True:
            rlist, wlist, e = select.select(self.conn, self.connection, self.conn, 0.05)

            for w in wlist:
                tpl = f'GET / HTTP/1.0\r\nHost:{w.host}\r\n\r\n'
                w.socket.send(bytes(tpl,encoding='utf-8'))
                print(w.host,'连接上了。。。。')
                self.connection.remove(w)

            for r in rlist:
                recv_data = bytes()
                while True:
                    try:
                        chunck = r.socket.recv(1024)
                        recv_data += chunck
                    except Exception as e:
                        break

                response = HttpResponse(recv_data)
                r.callback(response)
                r.socket.close()
                self.conn.remove(r)


            if len(self.conn) == 0:
                break

def f1(response):
    print(response.header_dict)

host_list = [
    {'host':'www.baidu.com','callback':f1},
    {'host': 'cn.bing.com', 'callback': f1},
]


aclient = AsynicClient()
for host in host_list:
    aclient.add_request(host['host'],host['callback'])

aclient.run()