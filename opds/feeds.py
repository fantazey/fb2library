# -*- coding: utf-8 -*-
__author__ = 'andrew'
__all__ = ['MainFeed',
           'AuthorsCharsFeed', 'AuthorsFeed', 'AuthorBooksFeed',
           'GenresFeed', 'GenreBooksFeed',
           'SequencesFeed', 'SequenceBooksFeed',
           'BookFeed']

from django.contrib.syndication.views import Feed

from opds.models import *
from opds.OPDSFeed import *
from book.models import *


class MainFeed(Feed):
    """ Главное меню OPDS """
    title = u"Главное меню"
    link = "/opds"
    feed_type = NaviFeed
    description = u"Главное меню каталога"

    def items(self):
        return MenuItem.objects.filter(group='0').order_by('order')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()


class AuthorsCharsFeed(Feed):
    """ Список букв фамилий авторов """
    title = u"Выбор автора"
    link = "/opds/authors/"
    feed_type = NaviFeed
    description = u"Меню с первыми буквами фамилий автора, " \
                  u"для оптимизации поиска"

    def items(self):
        return Char.objects.all().order_by('char')

    def item_title(self, item):
        return u"Авторы на %s" % item.char

    def item_description(self, item):
        return u"Авторы на %s" % item.char

    def item_link(self, item):
        return item.get_absolute_url()


class AuthorsFeed(Feed):
    """ Список авторов на букву """
    title = u"Список авторов на букву"
    link = "/opds/authors/"
    feed_type = NaviFeed
    description = u"Авторы, чьи фамилии начинаются на выбранную букву"

    def get_object(self, request, char_id):
        return Char.objects.get(id=char_id)

    def items(self, obj):
        return Author.objects.filter(last_name__startswith=obj.char).\
            order_by('last_name', 'first_name')

    def item_title(self, item):
        return item.__unicode__()

    def item_description(self, item):
        return item.__unicode__()

    def item_link(self, item):
        return item.get_absolute_url_opds()


class AuthorBooksFeed(Feed):
    """ Книги автора """
    title = u"Список книг автора"
    link = "/opds/authors/"
    feed_type = BookFeed
    description = u"Список книг автора"

    def get_object(self, request, author_id):
        return Author.objects.get(id=author_id)

    def items(self, obj):
        return Book.objects.filter(authors=obj).order_by('title')

    def item_title(self, item):
        return item.title

    def item_extra_kwargs(self, item):
        res = {}
        if item.genre.all().exists():
            genre = item.genre.all()[0]
            res['category_label'] = genre.name
            res['category_term'] = genre.code
        res['abs_link'] = item.get_absolute_url()
        res['cover_link'] = item.get_cover_url()
        res['cover_thumb_link'] = item.get_cover_url()
        res['download_link'] = item.get_download_url()
        return res

    def item_description(self, item):
        return '%s - %s' % (item.get_authors_string(), item.title)

    def item_link(self, item):
        return item.get_absolute_url_opds()


class GenresFeed(Feed):
    """ Список жанров """
    title = u"Список жанров"
    link = "/opds/genres/"
    feed_type = NaviFeed
    description = u"Список доступных жанров"

    def items(self):
        return Genre.objects.all().order_by('name')

    def item_title(self, item):
        return item.__unicode__()

    def item_description(self, item):
        return item.__unicode__()

    def item_link(self, item):
        return item.get_absolute_url_opds()


class GenreBooksFeed(AuthorBooksFeed):
    """ Список книг в жанре """
    title = u"Список книг в жанре"
    link = "/opds/genre/"
    feed_type = BookFeed
    description = u"Список книг в жанре"

    def get_object(self, request, genre_id):
        return Genre.objects.get(id=genre_id)

    def items(self, obj):
        return Book.objects.filter(genre=obj)


class SequencesFeed(Feed):
    """ Список серий книг """
    title = u"Список серий книг"
    link = "/opds/sequence/"
    feed_type = NaviFeed
    description = u"Список серий книг"

    def items(self):
        return Sequence.objects.all().order_by('name')

    def item_title(self, item):
        return item.__unicode__()

    def item_description(self, item):
        return item.__unicode__()

    def item_link(self, item):
        return item.get_absolute_url_opds()


class SequenceBooksFeed(AuthorBooksFeed):
    """ Книги из серии """
    title = u"Список книг серии"
    link = "/opds/sequences/"
    feed_type = BookFeed
    description = u"Список книг серии"

    def get_object(self, request, sequence_id):
        return Sequence.objects.get(id=sequence_id)

    def items(self, obj):
        return Book.objects.filter(sequence=obj).order_by('title')


class BookFeed(Feed):
    """ Пока неиспользуемый фид """
    title = "test"
    link = "/opds/authors/"
    feed_type = BookFeed
    description = "test main feed"

    def get_object(self, request, book_id):
        return Book.objects.get(id=book_id)

    def items(self, obj):
        return Book.objects.filter(authors=obj).order_by('title')

    def item_title(self, item):
        return item.title

    def item_extra_kwargs(self, item):
        res = {}
        if item.genre.all().exists():
            genre = item.genre.all()[0]
            res['category_label'] = genre.name
            res['category_term'] = genre.code
        res['abs_link'] = item.get_absolute_url()
        res['cover_link'] = item.get_cover_url()
        res['cover_thumb_link'] = item.get_cover_url()
        res['download_link'] = item.get_download_url()
        return res

    def item_description(self, item):
        return '%s - %s' % (item.get_authors_string(), item.title)

    def item_link(self, item):
        return item.get_absolute_url_opds()
