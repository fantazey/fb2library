# -*- coding: utf-8 -*-
import os
from BeautifulSoup import BeautifulStoneSoup
from genres import genres_types
from hashlib import md5

__author__ = 'Andrew'

"""
    Модуль позволяющий парсить fb2 книги в объекты классов представленных
    в модуле
    http://www.fictionbook.org/index.php/%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5_%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B0_FB2_%D0%BE%D1%82_Sclex
"""


class CommonTag(object):
    """
    Общие методы работы с обьектами Tag
    """
    @staticmethod
    def get_node_attrs(node):
        """
        Вытаскивает аттрибуты ноды как нормальный словарь, а не как понос
        :param node: экземпляр класса Tag, аттибуты которого хотим знать
        :return: словарь с аттрибутами
        """
        return {x[0]: x[1] for x in node.attrs}

    def node_has_attr_like(self, node, like):
        """
        Проверка наличия у ноды атрибута с именем похожим на like
        :param node:  нода, аттрибуты которой проверяем
        :param like: строка, которую ищем в названии аттрибута
        :return: True если есть аттрибут с похожим названием, False иначе
        """
        attrs = self.get_node_attrs(node)
        return any([x.find(like) >= 0 for x in attrs.keys()])

    def get_node_attr_like(self, node, like):
        """
        Выполняет поиск и возвращает имя атрибута похожего на like
        :param node: нода в которой идет поиск аттрибута
        :param like: строка, которая ищется в названии аттрибута
        :return: название аттрибута в результате поиска
        """
        attrs = self.get_node_attrs(node)
        attr = None
        for x in attrs.keys():
            if x.find(like) >= 0:
                attr = x
        return attr


class BookFile(CommonTag):
    """
        Класс файла с книгой, в кострукторе класса реализуется разбиение файла
        на блоки, и создание необходимых классов
    """
    def __init__(self, path=None):
        # содержимое файла
        self.xml = ""
        # путь к файлу
        self.file = path
        # объект BeautifulStoneSoup и разобраная книга
        self.soup = self.book = None
        # новый путь для сохранения
        self.new_path = ""
        # новое имя файла
        self.new_name = ""
        # md5 hash от текста книги
        self.hash = ""

    def get_encoding(self):
        """Получить кодировку"""
        # пока это тупой поиск кодировки, так как BSS не всегда адекватно читает
        # её из файла и пытается угадывать что попало
        # пока проверяются только две кодировки
        # todo: future исправить на что-либо умное
        from re import search as regsearch
        encoding = regsearch("xml.*encoding=[\'\"]([0-9a-zA-Z-]+)[\"\']",
                             self.xml).groups()[0]
        if encoding.lower() in ["windows-1251", "cp1251"]:
            return 'windows-1251'
        elif encoding.lower() in ["utf-8", "utf8"]:
            return "utf-8"
        else:
            return None

    def get_cover(self):
        """
        Разбираем информацию об обложке
        """
        cover = None
        title_info = self.soup.description.find('title-info')
        # нода есть
        if title_info.coverpage and title_info.coverpage.image:
            image = title_info.coverpage.image
            # нода содержит аттрибут похожий на href
            if self.node_has_attr_like(image, 'href'):
                attr_name = self.get_node_attr_like(image, 'href')
                covername = image[attr_name].replace('#', '')
                # ищем среди binary нужный там тег
                binary = self.soup.find('binary', attrs={'id': covername})
                if binary:
                    cover = CoverPage()
                    # сохраняем base64 данные
                    cover.data = binary.contents[0]
                    cover.extension = covername.split('.')[-1]
                    cover_attrs = self.get_node_attrs(binary)
                    if 'content-type' in cover_attrs.keys():
                        cover.content_type = cover_attrs['content-type']
        return cover

    def make_book(self):
        """ Сделать экземплар объекта Book из файла
        :return: экземпляр класса Book,разобраный и провереный
        или None если возникла ошибка
        """
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
        finally:
            book_file.close()
        encoding = self.get_encoding()
        # не определили кодировку, выходим
        if encoding is None:
            return None
        self.soup = BeautifulStoneSoup(
            self.xml,
            fromEncoding=encoding,
            convertEntities=BeautifulStoneSoup.ALL_ENTITIES
        )
        self.book = Book()
        self.book.title_info = self.soup.description.find('title-info')
        self.book.encoding = encoding
        self.book.publish_info = self.soup.description.find('publish-info')
        self.book.parse()
        cover = self.get_cover()
        if cover is not None:
            self.book.cover = cover
        self.new_name, self.new_path = self.get_new_name_path()
        self.hash = md5(self.xml).hexdigest()
        return True

    def get_new_name_path(self):
        """Получить путь к файлу построенный на фамилии автора и названии книги"""
        stops = ',:><|?*/\n\\"'
        title = self.book.title
        if any([char in title for char in stops]):
            title = reduce(lambda res, y: res.replace(y, '-'), stops, title)
        author = self.book.authors[0]
        name = author.last_name + ' ' + author.first_name + " - " + title + ".fb2"
        author_dir = author.last_name + ' ' + author.first_name
        lang = self.book.lang if self.book.lang is not None else '#'
        if len(author.last_name) > 0:
            letter = author.last_name[0].upper()
        else:
            letter = '#'
        path = os.path.join(lang, letter, author_dir, name)
        return name, path


class CoverPage(object):
    """ Класс обложка """
    def __init__(self):
        # base64 кодированная строка
        self.data = ""
        # MIME тип изображения
        self.content_type = ""
        # расширение файла
        self.extension = ""


class Author(object):
    """ Класс автора.Автор """

    def __init__(self, first="", last="", middle=""):
        # имя
        self.first_name = first
        # фамилия
        self.last_name = last
        # отчество
        self.middle_name = middle

    def __repr__(self):
        return u"".join([
            self.last_name,
            u"-",
            self.first_name,
            u"-",
            self.middle_name
        ]).encode('utf-8')

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
    """
    Класс Переводчик
    Поля идентичны классу Author, поэтому пустой
    Разделение идет чисто по содержимому
    """
    def __init__(self, *args, **kwargs):
        super(Translator, self).__init__(*args, **kwargs)


class Genre(object):
    """ Класс Жанр """
    def __init__(self, code=""):
        # код жанра, ex: love_contemporary
        self.code = code
        # описание, на самом деле будет пустым почти постоянно, скорее всего
        if code in genres_types.keys():
            self.name = genres_types[code]
        else:
            self.name = None

    def __repr__(self):
        if self.name is not None:
            return self.name.encode("utf-8")
        else:
            return self.code.encode("utf-8")


class Sequence(object):
    """ Класс Серия """
    def __init__(self, name=""):
        # название серии
        self.name = name
        # номер книги в серии
        self.number = ""

    def __repr__(self):
        return self.name.encode("utf-8")


class Book(CommonTag):
    """ Класс книги """
    def __init__(self):
        # Название книги
        self.title = None
        # аннотация
        self.annotation = None
        # дата
        self.date = None
        # язык
        self.lang = None
        # исходных язык
        self.src_lang = None
        # обложка хранится base64 строкой
        self.cover = None
        # список авторов
        self.authors = []
        # серии в которые включена книга
        self.sequences = []
        # жанры книги
        self.genres = []
        # переводчики книги
        self.translators = []
        # исходная строка с данными о книге
        self.title_info = None
        # исходная строка с данными об издателе
        self.publish_info = None
        # информация об издательстве и издании
        self.publisher = None
        # кодировка книги
        self.encoding = None
        self.uuid = None

    def __repr__(self):
        return self.title.encode("utf-8")

    def parse(self):
        """
        Парсим блоки title_info и publish_info
        собираем объект книги и со всем сопутствующим
        """
        self.parse_authors(_type='author')
        self.parse_authors(_type='translator')
        self.parse_genres()
        self.parse_sequence()
        self.parse_other()
        self.parse_publisher()

    def parse_authors(self, _type='author'):
        """
        Вытаскиваем информацию об авторах или переводчиках и
        сохраняет в соотвествующем поле
        :param _type: тип разбираемой информации. авторы (author) или
        переводчики (translators)
        """
        if _type == 'author':
            object_class = Author
            field = 'authors'
        elif _type == 'translator':
            object_class = Translator
            field = 'translators'
        else:
            return
        authors_list = self.title_info.findAll(_type)
        if len(authors_list) == 0 and _type == 'author':
            author = object_class("#", "#", "#")
            self.__dict__[field].append(author)
        else:
            for _author in authors_list:
                # вытаскиваем словарь данных
                data = self.get_author_names(_author)
                author = object_class(
                    data['first'],
                    data['last'],
                    data['middle']
                )
                author.format_names()
                self.__dict__[field].append(author)

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
            else:
                data[n] = ''
        return data

    def parse_genres(self):
        """
        Вытаскиваем информацию о жанрах
        :return: True если не было ошибок при разборе
        """
        for genre in self.title_info.findAll('genre'):
            if genre.string:
                self.genres.append(Genre(genre.string.strip()))

    def get_sequences(self, node):
        """
        Серии могут быть в различных секциях описания книги
        Поэтому метод вынесен отдельно.
        :param node: родительская нода, в которой ведем поиск информации о серии
        :return: список объектов Sequence, которые были найдены в node
        """
        sequences = node.findAll('sequence')
        data = []
        if sequences:
            for seq in sequences:
                sequence = None
                attrs = self.get_node_attrs(seq)
                if 'name' in attrs.keys():
                    sequence = Sequence(attrs['name'])
                if 'number' in attrs.keys() and sequence:
                    sequence.number = attrs['number']
                if sequence is not None:
                    data.append(sequence)
        return data

    def parse_sequence(self):
        """
        Вытаскиваем информацию о сериях
        :return: True если не было ошибок при разборе
        """
        self.sequences = self.get_sequences(self.title_info)

    @staticmethod
    def get_tag_text(tag_name, node):
        """
        Получить текст-содержимое тэга
        :param tag_name: - имя тэга, содержимое которого будем вытаскивать
        :param node: родительская нода в которой выполняется поиск тэга
        """
        if node.find(tag_name) and node.find(tag_name).string:
            return node.find(tag_name).string.strip()
        else:
            return None

    def parse_other(self):
        """
        Вытаскиваем оставшуюся информацию:
        язык, дату,аннотацию, название
        :return: True если не было ошибок при разборе
        """
        self.title = self.get_tag_text('book-title', self.title_info)
        self.date = self.get_tag_text('date', self.title_info)
        self.lang = self.get_tag_text('lang', self.title_info)
        self.src_lang = self.get_tag_text('src-lang', self.title_info)
        # Аннтотация
        if self.title_info.annotation and self.title_info.annotation.contents:
            self.annotation = self.title_info.annotation.__str__()

    def parse_publisher(self):
        """
        Вытаскиваем оставшуюся информацию:
        язык, дату,аннотацию, название
        :return: True если не было ошибок при разборе
        """
        publisher_info = PublishInfo()
        if self.publish_info:
            publisher_name = self.get_tag_text('publisher', self.publish_info)
            if publisher_name is not None:
                publisher_info.publisher = Publisher(publisher_name)
            publisher_info.city = self.get_tag_text('city', self.publish_info)
            publisher_info.year = self.get_tag_text('year', self.publish_info)
            publisher_info.isbn = self.get_tag_text('isbn', self.publish_info)
            publisher_info.sequences = self.get_sequences(self.publish_info)
        self.publisher = publisher_info


class Publisher(object):
    """
    Класс Издатель
    """
    def __init__(self, name=""):
        self.name = name

    def __repr__(self):
        return self.name.encode("utf-8")


class PublishInfo(object):
    """
    Класс Информация об издании
    """
    def __init__(self):
        self.publisher = self.year = self.city = self.isbn = None
        self.sequences = []

    def __repr__(self):
        if self.publisher:
            return self.publisher.__repr__()