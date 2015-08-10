# -*- coding: utf-8 -*-
__author__ = 'Andrew'
# Класс для работы с книгами FB2.
# http://www.fictionbook.org/index.php/%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5_\
# %D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B0_FB2_%D0%BE%D1%82_Sclex
# VERSION 0.0.1
import os
from datetime import datetime
from BeautifulSoup import BeautifulStoneSoup

# TODO: 1 Перехват исключений
# TODO: 2 Обложки сохраняются битыми
LOG = '/home/andrew/projects/_fb2to/log.txt'


class FBook:
    """ Класс для работы с книгами FB2. Считывает из книги кодировку,
    авторов, название. Все данные хранятся в unicode """
    def __init__(self, file_name, level=0, logger=None):
        """ В конструктор передается текст книги
        :param file_name: полный путь к файлу
        :param level: уровень валидации книг
        :param logger: объект логгер для записи действий
        """
        self.logger = logger
        self.filename = file_name
        self.title_info = {
            'genre': [],
            'book-title': u'',
            'annotation': u'',
            'date': u'',
            'lang': u'',
            'src-lang': u'',
            'coverpage': {},
            'authors': [],
            'sequence': [],
            'translator': []
        }
        self.publish_info = {
            'publisher': u'',
            'year': u'',
            'city': u'',
            'isbn': u'',
            'sequence': []
        }
        self.book = self.encoding = self.soup = None
        self.description = self.t_info = self.p_info = None
        self.book_file_name = self.book_file_path = None
        self.level = level
        self.valid = False
        try:
            res, error_description = self.main()
        except Exception, e:
            self.logger.error(e.message)
            res = -1
            error_description = e.message

        if res == 0:
            self.validate()
            if self.valid:
                self.logger.info(u"Build new filename")
                self.get_new_filename()
            else:
                self.error = True
                self.error_description = u'Book not valid'
        else:
            self.error = True
            self.error_description = error_description

    def __str__(self):
        if self.book_file_name:
            return self.book_file_name
        else:
            return self.filename

    def __unicode__(self):
        if self.book_file_name:
            return self.book_file_name
        else:
            return self.filename

    def main(self):
        # Читаем книгу
        book_file = open(self.filename, 'r')
        self.logger.debug(u"Read file: %s" % self.filename)
        try:
            self.book = book_file.read()
        except IOError as e:
            self.logger.error(u"Error reading file. Exception: ", e.errno, e.strerror)
            return self.filename, u"Read file error"
        # Определяем кодировку
        self.logger.debug(u"Read encoding")
        try:
            self.encoding = self.get_encoding()  # кодировка
            self.soup = BeautifulStoneSoup(self.book)
        except UnicodeError as e:
            # Ошибка кодировки
            self.logger.error(u"Error reading encoding. Exception: %s" % e.message)
            return self.filename, u"Read encoding error",
        # С кодировкой все хорошо. Разбираем книгу
        try:
            # Служебная секция
            self.description = self.soup.description
            # Информация о книге
            self.t_info = self.description.find('title-info')
            # Информация об издателе
            self.p_info = self.description.find('publish-info')
            if self.t_info:
                self.logger.debug(u"Parse title info section")
                self.parse_tinfo()
            else:
                self.logger.error(u"Missed title info")
                return self.filename, u"Missed TitleInfo tag"
            if self.p_info:
                self.logger.debug(u"Parse publisher info section")
                self.parse_pinfo()
        except Exception, e:
            self.logger.error(u"Book has errors.", e.message)
            return self.filename, u"Book has errors."
        return 0, ''

    def get_encoding(self):
        """Получить кодировку"""
        from re import search as regsearch
        encoding = regsearch("xml.*encoding=[\'\"]([0-9a-zA-Z-]+)[\"\']", self.book).groups()[0]
        if encoding.lower() in ["windows-1251", "cp1251"]:
            return 'windows-1251'
        elif encoding.lower() in ["utf-8", "utf8"]:
            return "utf-8"
        else:
            raise UnicodeError(u"Unknown encoding: ", encoding)

    def parse_tinfo(self):
        """
        Разбираем информацию о названии, авторах, жанрах
        """
        for genre in self.t_info.findAll('genre'):
            if genre.string:
                self.title_info['genre'].append(genre.string.strip())
        # Название книги
        self.title_info['book-title'] = self.get_tag_text('book-title', self.t_info)
        self.title_info['date'] = self.get_tag_text('date', self.t_info)
        self.title_info['lang'] = self.get_tag_text('lang', self.t_info)
        self.title_info['src-lang'] = self.get_tag_text('src-lang', self.t_info)
        # Аннтотация
        if self.t_info.annotation and self.t_info.annotation.contents:
            self.title_info['annotation'] = self.t_info.annotation.renderContents()
        if self.t_info.coverpage and self.t_info.coverpage.image:
            if 'href' in self.t_info.coverpage.image.attrs[0][0]:
                covername = self.t_info.coverpage.image.attrs[0][1].replace('#', '')
                binary = self.soup.find('binary', attrs={'id': covername})
                if binary:
                    self.title_info['coverpage']['ext'] = covername.split('.')[-1]
                    for attr in binary.attrs:
                        if 'type' in attr[0]:
                            self.title_info['coverpage']['type'] = attr[1]
                        if 'id' in attr[0] and attr[1] == covername:
                            self.title_info['coverpage']['data'] = binary.text.strip()

        # Список авторов
        self.title_info['authors'] = self.get_authors('author')
        # Список переводчиков
        self.title_info['translator'] = self.get_authors('translator')
        # необязательное поле серия
        sequences = self.t_info.findAll('sequence')
        if sequences:
            self.logger.debug(u"Find sequences: ", str(sequences))
        for seq in sequences:
            self.title_info['sequence'].append({attr[0]: attr[1].strip() for attr in seq.attrs})
        return 0

    @staticmethod
    def get_tag_text(tag_name, section):
        if section.find(tag_name) and section.find(tag_name).string:
            return section.find(tag_name).string.strip()
        else:
            return ''

    def get_authors(self, _type):
        """Получить список авторов книги"""
        authors = []
        author_l = self.t_info.findAll(_type)
        for author in author_l:
            first_name, middle_name, last_name = '', '', ''
            if author.find('first-name') and author.find('first-name').string:
                first_name = hetu(author.find('first-name').string.strip())
                first_name = first_name[0].upper() + first_name[1:].lower()
            if author.find('middle-name') and author.find('middle-name').string:
                middle_name = hetu(author.find('middle-name').string.strip())
                middle_name = middle_name[0].upper() + middle_name[1:].lower()
            if author.find('last-name') and author.find('last-name').string:
                last_name = hetu(author.find('last-name').string.strip())
                last_name = last_name[0].upper() + last_name[1:].lower()
            authors.append((first_name, middle_name, last_name))
        return authors

    def parse_pinfo(self):
        """
        Разбираем информацию об издателе
        """
        self.publish_info['publisher'] = self.get_tag_text('publisher', self.p_info)
        self.publish_info['city'] = self.get_tag_text('city', self.p_info)
        self.publish_info['year'] = self.get_tag_text('year', self.p_info)
        self.publish_info['isbn'] = self.get_tag_text('isbn', self.p_info)
        for seq in self.p_info.findAll('sequence'):
            self.publish_info['sequence'].append({attr[0]: attr[1].strip() for attr in seq.attrs})
        return 0

    def validate(self):
        # Самый строгий уровень
        # Обязательные поля:
        # - фио автора
        # - жанр
        # - дата
        # - язык
        # - аннотация
        valid = True
        if self.level == 0:
            if not self.title_info['genre']:
                valid = False
            if not self.title_info['lang']:
                valid = False
            if not self.title_info['authors']:
                valid = False
            else:
                for _author in self.title_info['authors']:
                    if len(_author[0]) == 0 or len(_author[1]) == 0 or len(_author[2]) == 0:
                        valid = False
            if not self.title_info['annotation']:
                valid = False
        elif self.level == 1:
            if not self.title_info['genre']:
                valid = False
            if not self.title_info['authors'] or not any([_author[2] for _author in self.title_info['authors']]):
                valid = False
        self.valid = valid
        return 0

    def get_new_filename(self):
        """Получить путь к файлу построенный на фамилии автора и названии книги"""
        stops = ',:><|?*/\n\\"'
        title = self.title_info['book-title']
        if any([char in title for char in stops]):
            title = reduce(lambda res, y: res.replace(y, '-'), stops, title)
        author = ''
        for _author in self.title_info['authors']:
            if _author[0] and _author[2]:
                author = _author
        if self.level == 0:
            name = author[2] + ' ' + author[0] + " - " + title + ".fb2"
            author_dir = author[2] + ' ' + author[0]
        else:
            name = author[2] + " - " + title + ".fb2"
            author_dir = author[2]
        if 'lang' in self.title_info.keys():
            lang = self.title_info['lang']
        else:
            lang = 'unknown'
        letter = author[2][0].upper()
        path = os.path.join(lang, letter, author_dir, name)
        self.book_file_name = name
        self.book_file_path = path


def hetu(text):
    """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    return unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
