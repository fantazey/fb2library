# -*- coding: utf-8 -*-
__author__ = 'Andrew'

"""
    Модуль позволяющий парсить fb2 книги в словари
"""


class BookFile(object):
    """
        Класс файла с книгой, в кострукторе класса реализуется разбиение файла
        на блоки и возврат необходимых блоков в дочерние классы
    """
    def __init__(self, file_object=None):
        self.xml = ''

    def make_book(self):
        """
        Метод создающий объект книги из полученого файла
        :return:
        """

class Author(object):
    """ Класс автора.Автор """
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.middle_name = ""
        pass


class Genre(object):
    def __init__(self):
        self.code = ""


class Sequence(object):
    def __init__(self):
        self.name = ""
        self.number = ""


class Book(object):
    """ Класс книги """
    def __init__(self):
        self.title = ""
        self.annotation = ""
        self.date = ""
        self.lang = ""
        self.src_lang = ""
        self.cover = ""
        self.authors = []лk
        self.sequences = []
        self.translators = []
        self.title_info_source = ""
        self.publish_info_source = ""
        self.encoding = ""