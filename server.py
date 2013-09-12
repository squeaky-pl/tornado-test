from __future__ import print_function

from functools import partial
from traceback import print_exc

from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop
from tornado.gen import coroutine, Task, Return


def read(client, data):
    print(client['address'], data)


@coroutine
def throw():
    1/0

    raise Return()


@coroutine
def handle(client, stream):
    client_read = partial(read, client)

    while True:
        data = yield Task(stream.read_until, '{')
        data = data[:-1]
        count = int(data.strip()) - 1
        print('Reading {0} bytes.'.format(count))
        data = '{' + (yield Task(stream.read_bytes, count))
        client_read(data)

        if data == '{x}':
            break


class EchoServer(TCPServer):
    @coroutine
    def handle_stream(self, stream, address):
        self.clients = {}

        print(address)

        self.clients[address] = client = {'address': address}

        try:
            yield handle(client, stream)
        except Exception:
            print_exc()
            raise

        stream.close()
        raise Return()

server = EchoServer()
server.listen(65000)

IOLoop.instance().start()
