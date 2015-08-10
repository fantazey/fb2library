# -*- coding: utf-8 -*-
__author__ = 'andrew'

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from opds.models import *
from book.models import *
from book.OPDSFeed import OPDS


class OPDSFeed(Feed):
    feed_type = OPDS
    mime_type = 'application/xml'


class MainMenuFeed(OPDSFeed):
    """ Главное меню """
    title = "Main menu"
    alt_link = "/opds"
    link = "/opds"
    description = "Main menu of opds"
    model = MenuItem

    def items(self):
        return self.model.objects.filter(group="main").order_by('order')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return "%s/%s" % (self.link, item.link)

    def get_context_data(self, **kwargs):
        context = super(MainMenuFeed, self).get_context_data(**kwargs)
        context['foo'] = 'bar'
        return context

class GenreCharsFeed(OPDSFeed):
    """ Жанры по буквам """
    title = "Search genre"
    link = "/opds/search-genre"
    description = "Search by genre first character"

    def items(self):
        char_ids = []
        for g in Genre.objects.all():
            _ch = g.code[0].upper()
            if Char.objects.filter(char=_ch).exists():
                char_ids.append(Char.objects.filter(char=_ch)[0].id)
        return Char.objects.filter(id__in=char_ids).order_by("char")

    def item_title(self, item):
        return item.char

    def item_description(self, item):
        return u"Genres on letter: %s" % item.char

    def item_link(self, item):
        return "%s/%s" % (self.link, item.id)


class AuthorCharsFeed(OPDSFeed):
    """ Поиск авторов по буквам """
    title = "Authors by char list"
    link = "/opds/search-author"
    description = "List of authors with search by char"

    def items(self):
        char_ids = []
        for a in Author.objects.all():
            if a.last_name is not None and len(a.last_name) > 0:
                _ch = a.last_name[0].upper()
            else:
                _ch = u"U"
            if Char.objects.filter(char=_ch).exists():
                char_ids.append(Char.objects.filter(char=_ch)[0].id)
        return Char.objects.filter(id__in=char_ids).order_by("char")

    def item_title(self, item):
        return item.char

    def item_description(self, item):
        return u"Authors on letter: %s" % item.char

    def item_link(self, item):
        return "%s/%s" % (self.link, item.id)


class GenresByCharFeed(OPDSFeed):

    description = "Search by genre first character"

    def title(self, obj):
        return u"List genres on char %s" % obj.char

    def link(self, obj):
        return u"/opds/search-genre/%s" % obj.id

    def get_object(self, request, char_id, *args, **kwargs):
        return get_object_or_404(Char, id=char_id)

    def items(self, char):
        _char = char.char.lower()
        genres = list(Genre.objects.filter(code__startswith=_char))
        for genre in genres:
            genre.char_id = char.id
        return genres

    def item_title(self, item):
        return item.code

    def item_description(self, item):
        return item.code

    def item_link(self, item):
        return u"/opds/genre/%s" % item.id


class AuthorsByCharFeed(OPDSFeed):

    description = "Search authors by first character"

    def title(self, obj):
        return u"List authors on char %s" % obj.char

    def link(self, obj):
        return u"/opds/search-author/%s" % obj.id

    def get_object(self, request, char_id, *args, **kwargs):
        return get_object_or_404(Char, id=char_id)

    def items(self, character):
        _char = character.char.upper()
        return Author.objects.filter(last_name__startswith=_char)

    def item_title(self, item):
        return item.__unicode__()

    def item_description(self, item):
        return item.__unicode__()

    def item_link(self, item):
        return u"/opds/author/%s" % item.id


class BookByGenreFeed(OPDSFeed):
    description = "Books with genre"

    def title(self, obj):
        return u"Books with genre %s" % obj.code

    def link(self, obj):
        return u"/opds/genre/%s" % obj.id

    def get_object(self, request, genre_id, *args, **kwargs):
        return get_object_or_404(Genre, id=genre_id)

    def items(self, genre):
        return Book.objects.filter(genre=genre)

    def item_title(self, item):
        if item.authors.all().count() > 0:
            author = item.authors.all()[0].__unicode__()
        else:
            author = "Unknown"
        return u"%s - %s" % (author, item.title)

    def item_description(self, item):
        return item.title

    def item_link(self, item):
        return u"/opds/book/%s" % item.id


class BookByAuthorFeed(OPDSFeed):
    """ Книги автора """

    description = "Books with genre"

    def title(self, obj):
        return u"Books written by %s %s" % (obj.last_name, obj.first_name)

    def link(self, obj):
        return u"/opds/author/%s" % obj.id

    def get_object(self, request, author_id, *args, **kwargs):
        return get_object_or_404(Author, id=author_id)

    def items(self, author):
        return Book.objects.filter(authors=author)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.title

    def item_link(self, item):
        return u"/opds/book/%s" % item.id

    def item_extra_kwargs(self, obj):
        return {
          'foz': obj.some_method(),
          'baz': obj.some_attribute,
        }