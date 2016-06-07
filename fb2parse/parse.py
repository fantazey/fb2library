# -*- coding: utf-8 -*-

from datetime import datetime
from Queue import Queue
from fb2parse import worker
from settings import SOURCE, LOG_TEST


###
# todo: refactor this code
# Here we try to search books in SOURCE and start few process to parse them

def report_test(*args):
    """ Log all actions
    :param args: Strings for log. The first one define class(INF|DBG|ERR)
    :return:
    """
    with open(LOG_TEST, 'a') as log:
        _class = args[0]
        data = " ".join('%s' % a for a in args[1:])
        log.write("%s [%s] %s\n" % (
            _class,
            datetime.now().strftime('%y-%m-%d %H:%M:%S'),
            data
        ))


def multiple():
    _readers = _loaders = []
    for _x in range(20):
        _reader = worker.Worker(
            file_queue=files_queue,
            book_queue=book_queue,
            _type=worker.Worker.READER_TYPE,
            wid=_x
        )
        _reader.start()
        _readers.append(_reader)
    for _x in range(20, 40):
        _loader = worker.Worker(
            file_queue=files_queue,
            book_queue=book_queue,
            _type=worker.Worker.LOADER_TYPE,
            wid=_x
        )
        _loader.start()
        _loaders.append(_loader)
    return _readers, _loaders


# Script for testing threaded reading
if __name__ == "__main__":
    worker.make_project_dirs()
    report_test("INF", "Make directories")
    report_test("INF", "Directories created")
    files_queue = Queue(1000)
    book_queue = Queue(1000)
    report_test("INF", "Start walker")
    walker = worker.Walker(SOURCE, files_queue)
    walker.start()
    report_test("INF", "Run workers")
    _reader = worker.Worker(
        file_queue=files_queue,
        book_queue=book_queue,
        _type=worker.Worker.READER_TYPE,
        wid=1
    )
    _reader.start()
    _reader = worker.Worker(
        file_queue=files_queue,
        book_queue=book_queue,
        _type=worker.Worker.READER_TYPE,
        wid=2
    )
    _reader.start()
    _reader = worker.Worker(
        file_queue=files_queue,
        book_queue=book_queue,
        _type=worker.Worker.READER_TYPE,
        wid=3
    )
    _reader.start()
    _loader = worker.Worker(
        file_queue=files_queue,
        book_queue=book_queue,
        _type=worker.Worker.LOADER_TYPE,
        wid=4
    )
    _loader.start()
    _loader = worker.Worker(
        file_queue=files_queue,
        book_queue=book_queue,
        _type=worker.Worker.LOADER_TYPE,
        wid=5
    )
    _loader.start()

    # readers, loaders = multiple()
    # if not all([x.isAlive() for x in loaders]) or
    # not all([x.isAlive() for x in readers]):
    #     print "Finish"
