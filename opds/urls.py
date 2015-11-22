__author__ = 'Andrew'

from django.conf.urls import patterns, url
from opds.feeds import *

urlpatterns = patterns('/opds',
    url(r'^main/$', MainFeed()),
    url(r'^authors/$', AuthorsCharsFeed()),
    url(r'^authors/(?P<char_id>\d+)/$', AuthorsFeed()),
    url(r'^author/(?P<author_id>\d+)/$', AuthorBooksFeed()),
    url(r'^genres/$', GenresFeed()),
    url(r'^genre/(?P<genre_id>\d+)$', GenreBooksFeed()),
    url(r'^sequences/$', SequencesFeed()),
    url(r'^sequence/(?P<sequence_id>\d+)/$', SequenceBooksFeed()),
    url(r'^book/(?P<book_id>)\d+$', BookFeed())
)