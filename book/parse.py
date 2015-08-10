# -*- coding: utf-8 -*-
__author__ = 'Andrew'
import os
from datetime import datetime
from Queue import Queue
import worker
# Начало библиотеки. Все будет складываться сюда.
#PROJECT_ROOT = '/home/andrew/projects/_fb2to'
#SOURCE = '/home/andrew/projects/_fb2from'
PROJECT_ROOT = 'D:\\Projects\\proj\\_fb2to'
SOURCE = 'D:\\Projects\\proj\\_fb2from'
LOG = os.path.join(PROJECT_ROOT, "log.txt")
# Лог функции запуска
LOG_TEST = os.path.join(PROJECT_ROOT, "log_main.txt")


def report_test(*args):
    """ Логгирование действий и событий
    :param args: набор строк для вывода
    :return:
    """
    with open(LOG_TEST, 'a') as log:
        _class = args[0]
        data = " ".join('%s' % a for a in args[1:])
        log.write("%s [%s] %s\n" % (_class, datetime.now().strftime('%y-%m-%d %H:%M:%S'), data))


def multiple():
    _readers = _loaders = []
    for _x in range(20):
        _reader = worker.Worker(file_queue=files_queue, book_queue=book_queue, _type=worker.Worker.READER_TYPE, wid=_x)
        _reader.start()
        _readers.append(_reader)
    for _x in range(20, 40):
        _loader = worker.Worker(file_queue=files_queue, book_queue=book_queue, _type=worker.Worker.LOADER_TYPE, wid=_x)
        _loader.start()
        _loaders.append(_loader)
    return _readers, _loaders

if __name__ == "__main__":
    # очередь файлов
    worker.make_project_dirs()
    report_test("INF", "Make directories")
    report_test("INF", "Directories created")
    files_queue = Queue(1000)
    # очередь с книгами
    book_queue = Queue(1000)
    report_test("INF", "Start walker")
    walker = worker.Walker(SOURCE, files_queue)
    walker.start()
    report_test("INF", "Run workers")
    _reader = worker.Worker(file_queue=files_queue, book_queue=book_queue, _type=worker.Worker.READER_TYPE, wid=1)
    _reader.start()
    _reader = worker.Worker(file_queue=files_queue, book_queue=book_queue, _type=worker.Worker.READER_TYPE, wid=2)
    _reader.start()
    _reader = worker.Worker(file_queue=files_queue, book_queue=book_queue, _type=worker.Worker.READER_TYPE, wid=3)
    _reader.start()
    _loader = worker.Worker(file_queue=files_queue, book_queue=book_queue, _type=worker.Worker.LOADER_TYPE, wid=4)
    _loader.start()
    _loader = worker.Worker(file_queue=files_queue, book_queue=book_queue, _type=worker.Worker.LOADER_TYPE, wid=5)
    _loader.start()

    # readers, loaders = multiple()
    # if not all([x.isAlive() for x in loaders]) or not all([x.isAlive() for x in readers]):
    #     print "Finish"

