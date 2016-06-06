# -*- coding: utf-8 -*-

import os
import shutil
from threading import Thread
from time import sleep
import hashlib
from base64 import b64decode
import django
os.environ["DJANGO_SETTINGS_MODULE"] = "fb2lib.settings"
django.setup()
from book.models import *
from book.logger import Logger


# Логи потоков
LOG_FOLDER = os.path.join(PROJECT_ROOT, "Logs")
LIB_ROOT = os.path.join(PROJECT_ROOT, "Root")
BROKEN = os.path.join(LIB_ROOT, "Broken")
# Книги в которых нет обязательных данных.
BROKEN_BOOKS = os.path.join(BROKEN, "Books")
# Книги которые не получилось прочитать.
BROKEN_FILES = os.path.join(BROKEN, "Files")
# Обложки книг
COVERS = os.path.join(LIB_ROOT, "Covers")
# Библиотека
LIBRARY = os.path.join(LIB_ROOT, "Library")
# Дубли
DUPLICATE = os.path.join(LIB_ROOT, "Duplicate")
# Каталог, который содержит книги для разбора


def make_project_dirs():
    """ Создаем необходимые каталоги """
    for directory in [LIB_ROOT, BROKEN, BROKEN_BOOKS, BROKEN_FILES,
                      COVERS, LIBRARY, DUPLICATE, LOG_FOLDER]:
        if not os.path.exists(directory):
            os.makedirs(directory)


class Walker(Thread):
    """
    Класс выполняющий спокойную пешую прогулку по каталогам.
    В случае обнаружения книги, он складывает название файла в очередь.
    """
    def __init__(self, source_folder, queue):
        super(Walker, self).__init__()
        self.logger = Logger(u"walker", LOG_FOLDER)
        self.logger.info(u"Logger initialized. Walker")
        self.source = source_folder
        self.queue = queue

    def run(self):
        """
         Двигаться по каталогу. Если архив - отдали работнику.
         Если книга - добавили в очередь
        """
        for (_dir, sub_dir, files_here) in os.walk(self.source):
            for _file in files_here:
                while True:
                    if self.queue.full():
                        self.logger.debug(u"Full queue. Wait")
                        sleep(10)
                    else:
                        _path = os.path.join(_dir, _file)
                        self.logger.info(u"Add file:", _path)
                        self.queue.put(_path)
                        break
            self.logger.info(u"Finish")


class Worker(Thread):
    """
    Рабочий. Выполняет обработку книг. Сохранение их в нужном месте
    Рабочий с типом 1  перебирает файлы из очереди,
    если находит fb2 то пытается обработать его, чтобы получить FBook объект.
    Рабочий с типом 2 должен загружать информацию о найденных книгах в
    базу данных.
    Рабочий с типом 3 должен тоже чтото делать, но у него пока перекур.
    """
    READER_TYPE = 1
    LOADER_TYPE = 2
    NONE_TYPE = 3

    def __init__(self, file_queue, book_queue,  _type=3, wid=0):
        super(Worker, self).__init__()
        self.book_queue = book_queue
        self.file_queue = file_queue
        self.type = _type
        self.logger = Logger(wid, LOG_FOLDER)
        self.logger.info(
            u"Logger initialized. Worker id:",
            str(wid),
            u". Type:",
            self.type
        )
        self.eq_counter = 0
        # штука с которой работать - имя файла, или уже объект FBook
        self.item = None
        self.stop = False

    def run(self):
        """ Переопределяем метод run базового класса """
        if self.type == Worker.READER_TYPE:
            while not self.stop:
                self.reader_work()
        elif self.type == Worker.LOADER_TYPE:
            while not self.stop:
                self.loader_work()
        return 0

    def reader_work(self):
        """ Основная задача Worker """
        if self.file_queue.empty():
            self.logger.debug(u"Empty queue. Waiting")
            self.eq_counter += 1
            if self.eq_counter > 20:
                self.eq_counter = 0
                # self.stop = True
            sleep(10)
            return
        self.item = self.file_queue.get()
        self.logger.info(u"Item:", self.item)
        # определяем тип файла
        if self.item is None:
            self.logger.error(u"Something gone wrong. Item is None")
            self.eq_counter += 1
            if self.eq_counter > 20:
                self.logger.error(u"20 times error. Stopping")
                self.stop = True
            return
        name, ext = os.path.splitext(self.item)
        if ext == '.fb2':
            self.logger.info(u"Parse book")
            try:
                result = self.parse_book()
            except Exception, e:
                self.logger.error(e.message)
                return
            if result['error']:
                # если ошибка возникла
                if isinstance(result['item'], FBook):
                    self.move_broken_book(result)
                else:
                    self.move_bad_file()
            else:
                self.item = result['item']
                self.logger.info(u"Moving book to lib")
                self.move_book()
                self.book_queue.put(self.item)
                self.item = None
        else:
            self.logger.debug(u"Strange file %s" % self.item)

    def loader_work(self):
        if self.book_queue.empty():
            self.logger.debug(u"Empty queue. Waiting")
            self.eq_counter += 1
            if self.eq_counter > 20:
                self.eq_counter = 0
                # self.stop = True
            sleep(10)
            return
        self.item = self.book_queue.get()
        try:
            self.add2db()
        except Exception, e:
            print e.message
            self.logger.error(
                u"Load book: ",
                self.item.title_info['book-title'],
                u"\nException:",
                e.message
            )

    def parse_book(self):
        book = FBook(self.item, level=0, logger=self.logger)
        error = True
        item = self.item
        # получилась книга?
        if isinstance(book, FBook):
            # книга без ошибок
            if not hasattr(book, 'error'):
                # она валидна
                if book.valid:
                    error = False
                    item = book
                    self.logger.info(u"Book %s is ok" % self.item)
                # невалидна
                else:
                    self.logger.error(u"Book %s not valid" % self.item)
            else:
                # книга с ошибками
                self.logger.error(
                    u"Book %s has error: %s" % (
                        self.item,
                        book.error_description
                    )
                )
        # не удалось распарсить
        else:
            self.logger.error(u"File %s has errors" % self.item)
        return {'error': error, 'item': item}

    def move_book(self):
        # Выстраиваем путь для книги +
        self.build_path()
        # Сохраняем файл в новом месте +
        move = self.save_book()
        # Сохраняем изорбажение в каталоге +
        self.save_img()
        if move == 0:
            self.logger.info(
                u"File moved successfully. Removing original file: ",
                self.item.filename
            )
            try:
                os.unlink(self.item.filename)
            except Exception, e:
                self.logger.error(
                    u"Error on removing original file.",
                    e.message
                )
        pass

    @staticmethod
    def get_path_elements(path):
        """ Разбираем путь на части """
        _path, _file = os.path.split(path)
        elements = []
        while 1:
            _path, folder = os.path.split(_path)
            if folder != '':
                elements.append(folder)
                if _path == "":
                    break
            else:
                if _path != "":
                    elements.append(_path)
                break
        elements.reverse()
        return elements

    def build_path(self):
        """ Строим дерево каталогов """
        path = self.item.book_file_path
        start_path = LIBRARY
        elements = self.get_path_elements(path)
        for el in elements:
            start_path = os.path.join(start_path, el)
            if not os.path.exists(start_path):
                try:
                    os.mkdir(start_path)
                except Exception, e:
                    self.logger.error(u"Build path error.", e.message)
                    return False
        return True

    def save_book(self):
        try:
            if os.path.exists(os.path.join(LIBRARY, self.item.book_file_path)):
                self.logger.debug(u"Book has duplicate.")
                res = self.move_duplicate(self.item)
            else:
                self.logger.info(
                    u"Save book to %s" % os.path.join(
                        LIBRARY,
                        self.item.book_file_path
                    )
                )
                file_path = os.path.join(LIBRARY, self.item.book_file_path)
                _file = open(file_path, 'w')
                _file.write(self.item.soup.prettify())
                _file.close()
                res = 0
        except Exception, e:
            self.logger.error(u"Error on saving book.", e.message)
            res = -1
        return res

    def move_duplicate(self, item):
        from time import time as timestamp
        name, ext = os.path.splitext(item.book_file_name)
        name += ' ' + str(timestamp()) + ext
        try:
            file_path = os.path.join(DUPLICATE, name)
            _file = open(file_path, 'w')
            _file.write(self.item.soup.prettify())
            _file.close()
            return 0
        except Exception, e:
            self.logger.error(
                u"Move duplicate book",
                item.book_file_name,
                e.message
            )
            self.move_bad_file()
            return -1

    def save_img(self):
        if 'data' not in self.item.title_info['coverpage']:
            return 0
        img_name = hashlib.md5(self.item.book).hexdigest()
        # first 4 chars of img_name define dir for cover
        start_path = os.path.join(COVERS, img_name[:4])
        if not os.path.exists(start_path):
            os.mkdir(start_path)
        try:
            file_name = img_name + '.' + \
                self.item.title_info['coverpage']['ext']

            file_name = os.path.join(start_path, file_name)
            data = self.item.title_info['coverpage']['data']
            try:
                b64data = b64decode(data)
                with open(file_name, 'w') as _img_file:
                    _img_file.write(b64data)
                self.item.cover_path = os.path.join(img_name[:4], img_name)
            except Exception, e:
                self.logger.error(u"Exception: ", e.message)
                delta = 4 if len(data) % 4 == 0 else len(data) % 4
                b64data = b64decode(data[:len(data)-delta])
                with open(file_name, 'w') as _img_file:
                    _img_file.write(b64data)
                self.item.cover_path = file_name
        except Exception, e:
            self.logger.error(
                u"Book file: ",
                self.item.title_info['book-title'],
                u" Exception: ",
                e.message
            )

    def add2db(self):
        """
        Добавляем книгу в базу.
        """
        book_md5 = hashlib.md5(self.item.book).hexdigest()
        # Добавляем книгу
        if not Book.objects.filter(md5=book_md5).exists():
            self.logger.info(u"Add new book to db. md5:", book_md5)
            book = Book.objects.create(
                title=self.item.title_info['book-title'],
                annotation=self.item.title_info['annotation'],
                date=self.item.title_info['date'],
                book_file=self.item.book_file_path,
                md5=book_md5
            )
            if hasattr(self.item, 'cover_path'):
                book.image = self.item.cover_path
                book.save()
        else:
            book = None
        _lang = u'unknown'
        _src_lang = u'unknown'
        if 'lang' in self.item.title_info.keys():
            _lang = self.item.title_info['lang']
        if 'src_lang' in self.item.title_info.keys():
            _src_lang = self.item.title_info['src-lang']
        self.logger.debug(
            u"Create lang objects for: %s %s" % (_lang, _src_lang)
        )
        if not Language.objects.filter(code=_lang).exists():
            book_lang = Language.objects.create(code=_lang)
        else:
            book_lang = Language.objects.get(code=_lang)
        if not Language.objects.filter(code=_src_lang).exists():
            book_src_lang = Language.objects.create(code=_src_lang)
        else:
            book_src_lang = Language.objects.get(code=_src_lang)
        if book:
            book.lang = book_lang
            book.src_lang = book_src_lang
            book.save()

        b_genres = self.item.title_info['genre']
        # Создаем жанры прочитанные в книге
        for b_genre in b_genres:
            self.logger.info(u"Create genre:", b_genre)
            genre, cr = Genre.objects.get_or_create(code=b_genre)
            if book:
                book.genre.add(genre)
        # Создаем авторов
        for a_tuple in self.item.title_info['authors']:
            self.logger.debug(
                u"Create author:",
                a_tuple[0],
                a_tuple[1],
                a_tuple[2]
            )
            author, cr = Author.objects.get_or_create(
                first_name=a_tuple[0],
                middle_name=a_tuple[1],
                last_name=a_tuple[2]
            )
            if book:
                book.authors.add(author)
        # добавляем переводчиков
        translators = self.item.title_info['translator']
        for t_tuple in translators:
            self.logger.debug(
                u"Create translator:",
                t_tuple[0],
                t_tuple[1],
                t_tuple[2]
            )
            translator, cr = Translator.objects.get_or_create(
                first_name=t_tuple[0],
                middle_name=t_tuple[1],
                last_name=t_tuple[2]
            )
            if book:
                book.translator.add(translator)
        # Создаем серии
        for b_sequence in self.item.title_info['sequence']:
            if 'name' in b_sequence:
                self.logger.debug(u"Create sequence: %s" % b_sequence['name'])
                sequence, cr = Sequence.objects.get_or_create(
                    name=b_sequence['name']
                )
                if 'number' in b_sequence:
                    self.logger.debug(
                        u"Book has # in sequence: %s" % b_sequence['number']
                    )
                    _seq_num = b_sequence['number']
                else:
                    _seq_num = None
                SequenceBook.objects.get_or_create(
                    book=book,
                    sequence=sequence,
                    number=_seq_num
                )

    def move_broken_book(self, params):
        """ Убрать битую книгу """
        from time import time as timestamp
        item = params['item']
        name, ext = os.path.splitext(item.filename)
        name += ' ' + str(timestamp()) + ext
        try:
            file_path = os.path.join(BROKEN_BOOKS, item.filename)
            _file = open(file_path, 'w')
            _file.write(self.item.soup.prettify())
            _file.close()
        except Exception, e:
            self.move_bad_file()
            self.logger.error(u"Move broken book error: %s" % e.message)

    def move_bad_file(self):
        """ Убрать битый файл """
        dst_path = os.path.join(BROKEN_FILES, os.path.split(self.item)[-1])
        shutil.move(self.item, dst_path)
        return -2

    def unpack(self):
        """ Распаковать ахрив """
        if self.item:
            pass
        # todo: check commented code
        # arch = ZipFile(self.item, 'r')
        # arch_name = os.path.split(self.item)[-1]
        # name = " ".join(arch_name.split('.')[:-1])
        # extr_path = os.path.join(BookSource, name)
        # if not os.path.exists(extr_path):
        #     os.makedirs(extr_path)
        # try:
        #     # распаковали архив
        #     arch.extractall(extr_path)
        #     # удаляем архив
        #     os.unlink(self.item)
        # except Exception, e:
        #     self.logger.log("ERR", "Extract archive error. %s" % e.message)
