# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from opds.models import *
from opds.OPDSFeed import *
from book.models import *


__all__ = ['MainFeed',
           'AuthorsCharsFeed', 'AuthorsFeed', 'AuthorBooksFeed',
           'GenresFeed', 'GenreBooksFeed',
           'SequencesFeed', 'SequenceBooksFeed',
           'BookFeed']

# Classes for implementing work with OPDS (RSS books catalog)


class MainFeed(Feed):
    """ Main Menu OPDS """
    title = u"Main Menu"
    link = "/opds"
    feed_type = NaviFeed
    description = u"Main menu"

    def items(self):
        return MenuItem.objects.filter(group='0').order_by('order')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()


class AuthorsCharsFeed(Feed):
    """ List of first chars of authors """
    title = u"Select letter"
    link = "/opds/authors/"
    feed_type = NaviFeed
    description = u"Select letter for list of authors, " \
                  u"whom last-names starts with"

    def items(self):
        return Char.objects.all().order_by('char')

    def item_title(self, item):
        return u"Last-names starts with %s" % item.char

    def item_description(self, item):
        return u"Last-names starts with %s" % item.char

    def item_link(self, item):
        return item.get_absolute_url()


class AuthorsFeed(Feed):
    """ List of authors, whom last-name starts with char """
    title = u"List of authors"
    link = "/opds/authors/"
    feed_type = NaviFeed
    description = u"List of authors, whom last-name starts with char"

    def get_object(self, request, *args, **kwargs):
        return Char.objects.get(id=args[0])

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
    """ Author books """
    title = u"List of books for author"
    link = "/opds/authors/"
    feed_type = BookFeed
    description = u"List of books for author"

    def get_object(self, request, *args, **kwargs):
        return Author.objects.get(id=args[0])

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
    """ List of genres """
    title = u"List of genres"
    link = "/opds/genres/"
    feed_type = NaviFeed
    description = u"List of available genres"

    def items(self):
        return Genre.objects.all().order_by('name')

    def item_title(self, item):
        return item.__unicode__()

    def item_description(self, item):
        return item.__unicode__()

    def item_link(self, item):
        return item.get_absolute_url_opds()


class GenreBooksFeed(AuthorBooksFeed):
    """ Books in the genre """
    title = u"List of books in the genre"
    link = "/opds/genre/"
    feed_type = BookFeed
    description = u"List of books in the genre"

    def get_object(self, request, *args, **kwargs):
        return Genre.objects.get(id=args[0])

    def items(self, obj):
        return Book.objects.filter(genre=obj)


class SequencesFeed(Feed):
    """ Books sequences """
    title = u"List of book sequences"
    link = "/opds/sequence/"
    feed_type = NaviFeed
    description = u"List of book sequences"

    def items(self):
        return Sequence.objects.all().order_by('name')

    def item_title(self, item):
        return item.__unicode__()

    def item_description(self, item):
        return item.__unicode__()

    def item_link(self, item):
        return item.get_absolute_url_opds()


class SequenceBooksFeed(AuthorBooksFeed):
    """ Books from sequence """
    title = u"List of books from sequence"
    link = "/opds/sequences/"
    feed_type = BookFeed
    description = u"Список книг серии"

    def get_object(self, request, *args, **kwargs):
        return Sequence.objects.get(id=args[0])

    def items(self, obj):
        return Book.objects.filter(sequence=obj).order_by('title')


class BookFeed(Feed):
    """ Book feed. temporarily unused """
    title = "Test feed"
    link = "/opds/authors/"
    feed_type = BookFeed
    description = "TestFeed"

    def get_object(self, request, *args, **kwargs):
        return Book.objects.get(id=args[0])

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
