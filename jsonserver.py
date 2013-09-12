from traceback import print_exc
from logging import getLogger

from tornado.tcpserver import TCPServer
from tornado.gen import coroutine, Task, Return
from tornado.ioloop import IOLoop


logger = getLogger(__name__)


@coroutine
def handle_stream(stream):
    while 1:
        header = yield Task(stream.read_until, '{')
        header = header[:-1]

        count = int(header.strip()) - 1
        payload = '{' + (yield Task(stream.read_bytes, count))


class JSONServer(TCPServer):
    @coroutine
    def handle_stream(self, stream, address):
        logger.info('Connected {0[0]} at {0[1]}.'.format(address))
        try:
            yield handle_stream(stream)
        except Exception:
            print_exc()
            raise

        stream.close()
        raise Return()


def main():
    server = JSONServer()
    logger.info('Starting server...')
    server.listen(65000)

    IOLoop.instance().start()


if __name__ == '__main__':
    main()
