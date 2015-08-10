__author__ = 'Andrew'

from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('/book',
    #url(r'^$', 'book.views.library', name='recent'),
    url(r'authors/(?P<letter>\w)$', author_letter, name='author_letter'),
    url(r'details/(?P<id>\d+)$', book_details, name='book_details'),
    url(r'author/(?P<id>\d+)/books/$', author_books, name='author_books'),
    url(r'genre/(?P<id>\d+)/books/$', genre_books, name='genre_books'),
)