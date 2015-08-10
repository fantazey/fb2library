# -*- coding: utf-8 -*-
import os
from BeautifulSoup import BeautifulStoneSoup

__author__ = 'Andrew'

"""
    Модуль позволяющий парсить fb2 книги в объекты классов представленных
    в модуле
"""


class BookFile(object):
    """
        Класс файла с книгой, в кострукторе класса реализуется разбиение файла
        на блоки, и создание необходимых классов
    """
    def __init__(self, path=None):
        self.xml = ""
        self.file = path
        self.soup = None
        self.book = None

    def get_encoding(self):
        """Получить кодировку"""
        from re import search as regsearch
        encoding = regsearch("xml.*encoding=[\'\"]([0-9a-zA-Z-]+)[\"\']",
                             self.xml).groups()[0]
        if encoding.lower() in ["windows-1251", "cp1251"]:
            return 'windows-1251'
        elif encoding.lower() in ["utf-8", "utf8"]:
            return "utf-8"
        else:
            return None

    def make_book(self):
        # если в конструктор передано имя файла и он существует
        # то пытаемся открыть его, иначе выходим
        if self.file is None or not os.path.exists(self.file):
            # нечего открыть
            return None
        book_file = open(self.file, 'r')
        try:
            self.xml = book_file.read()
        except IOError:
            # ошибка открытия файла - выходим
            return None
        encoding = self.get_encoding()
        # не определили кодировку, выходим
        if encoding is None:
            return None
        self.soup = BeautifulStoneSoup(
            self.book,
            fromEncoding=encoding,
            convertEntities=BeautifulStoneSoup.ALL_ENTITIES
        )
        self.book = Book()
        self.book.title_info = self.soup.description.find('title-info')
        self.book.encoding = encoding
        self.book.publish_info = self.soup.description.find('publish-info')
        res = self.book.parse()
        # если разобрали книгу без ошибок res = True
        if res:
            # заканчиваем
            return self.book
        else:
            return None


class Author(object):
    """ Класс автора.Автор """
    def __init__(self, first="", last="", middle=""):
        self.first_name = first
        self.last_name = last
        self.middle_name = middle

    def format_names(self):
        """
        Первый символ каждого поля делаем заглавным
        """
        self.first_name = self.format_name(self.first_name)
        self.last_name = self.format_name(self.last_name)
        self.middle_name = self.format_name(self.middle_name)

    @staticmethod
    def format_name(string):
        """
        выполняет text-transform: capitalize над строкой
        :param string: строка в которой заменяем первый символ на заглавный
        :return: измененную строку, если длина больше 1
        """
        if len(string) > 1:
            return string[0].upper() + string[1:].lower()
        else:
            return string


class Translator(Author):
    def __init__(self):
        super(Translator, self).__init__()


class Genre(object):
    """ Класс Жанр. Поля:
    code: код жанра
    name: расшифровка кода
    """
    def __init__(self):
        self.code = ""
        self.name = ""


class Sequence(object):
    """ Класс Серия. Поля:
        name: Название серии
        number: Номер книги в серии
    """
    def __init__(self):
        self.name = ""
        self.number = ""


class Book(object):
    """ Класс книги """
    def __init__(self):
        # Название книги
        self.title = ""
        # аннотация
        self.annotation = ""
        # дата
        self.date = ""
        # язык
        self.lang = ""
        # исходных язык
        self.src_lang = ""
        # обложка хранится base64 строкой
        self.cover = ""
        # список авторов
        self.authors = []
        # серии в которые включена книга
        self.sequences = []
        # жанры книги
        self.genre = []
        # переводчики книги
        self.translators = []
        # исходная строка с данными о книге
        self.title_info = None
        # исходная строка с данными об издателе
        self.publish_info = None
        # кодировка книги
        self.encoding = ""

    def parse(self):
        """
        Парсим блоки title_info и publish_info
        собираем объект книги и со всем сопутствующим
        :return: True если все хорошо распарсилось, False - если были ошибки
        """
        self.parse_authors(_type='author')
        self.parse_authors(_type='translator')
        self.parse_genres()
        self.parse_sequence()
        self.parse_other()
        self.parse_publisher()
        return False

    def parse_authors(self, _type='author'):
        """
        Вытаскиваем информацию об авторах или переводчиках и
        сохраняет в соотвествующем поле
        :param _type: тип разбираемой информации. авторы (author) или
        переводчики (translators)
        :return: True если не было ошибок при разборе
        """
        if _type == 'author':
            object_class = Author
            field = 'authors'
        elif _type == 'translator':
            object_class = Translator
            field = 'translators'
        else:
            return False
        authors_list = self.title_info.findAll(_type)
        for _author in authors_list:
            # вытаскиваем словарь данных
            data = self.get_author_names(_author)
            # если есть Имя и Фамилия - сохраняем
            if len(data['first']) > 0 and len(data['last']):
                author = object_class(data['first'], data['last'], data['middle'])
                author.format_names()
                self.__dict__[field].append(author)
            else:
                continue
        if len(self.authors) == 0:
            return False
        return True

    @staticmethod
    def get_author_names(node=None):
        """
        :param node: BeautifulStoneSoup нода содержащая информацию о человеке
        first,last,middle-names
        :return: возвращает словарь с данными
        """
        names = ['first', 'last', 'middle']
        data = {'first': '', 'last': '', 'middle': ''}
        for n in names:
            if node.find(n + '-name') and node.find(n + '-name').string:
                data[n] = node.find(n + '-name').string.strip()
        return data

    def parse_genres(self):
        """
        Вытаскиваем информацию о жанрах
        :return: True если не было ошибок при разборе
        """
        return False

    def parse_sequence(self):
        """
        Вытаскиваем информацию о сериях
        :return: True если не было ошибок при разборе
        """
        return False

    def parse_other(self):
        """
        Вытаскиваем оставшуюся информацию:
        язык, дату,аннотацию, название
        :return: True если не было ошибок при разборе
        """
        return False

    def parse_publisher(self):
        """
        Вытаскиваем оставшуюся информацию:
        язык, дату,аннотацию, название
        :return: True если не было ошибок при разборе
        """
        return False