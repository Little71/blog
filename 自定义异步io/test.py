import selectors
import socket
import threading


def accept(sock: socket.socket):
    conn, _ = sock.accept()
    conn.setblocking(False)
    selector.register(conn, selectors.EVENT_READ, _recv)


def _recv(conn: socket.socket):
    data = conn.recv(1024).decode().strip()
    msg = "your msg is {}".format(data).encode()
    conn.send(msg)


# 平台自适应
selector = selectors.DefaultSelector()

sock = socket.socket()

addr = ('127.0.0.1', 9999)
sock.bind(addr)
sock.listen()
sock.setblocking(False)
e = threading.Event()

key = selector.register(sock, selectors.EVENT_READ, accept)
print(key)  # fileobj fd event data和下面events的key一样


def work():
    while not e.is_set():
        # 事件不满足之前这里是阻塞的
        events = selector.select()
        # 如是多线程，还没满足事件之前，多线程不是一致就绪状态，只要在内核拷贝到进程之后才是就绪状态
        # 非就绪状态，就cpu不去调用它，如拷贝完成后，就满足了事件，就成了就绪状态，等待调用

        # 是key和mask的二元组列表
        if events:
            # e.set()
            print(events)
        # 遍历准备好的事件，然后去执行data
        for key, mask in events:
            # mask 事件掩码或者值即 0b01 或者 0b10
            print(key, mask)
            # 获取传入的data，即上面注册时候传入的data
            callable = key.data
            # 直接调用data，传入文件对象
            # 如果上面满足事件后执行的函数参数一致，就不用做判断
            callable(key.fileobj)


threading.Thread(target=work, name='select').start()


def main():
    while not e.is_set():
        cmd = input('>>>').strip()
        if cmd == 'quit':
            e.set()
            fobjs = []
            # 返回key文件描述符和value是key的字典映射
            for fd, key in selector.get_map().items():
                fobjs.append(fd)
            for fobj in fobjs:
                # 取消注册，传入文件描述符
                selector.unregister(fobj)
                fobj.close()  # 关闭文件描述符
            # 关闭select
            selector.close()


if __name__ == '__main__':
    main()
