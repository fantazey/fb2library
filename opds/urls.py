__author__ = 'Andrew'

from django.conf.urls import patterns, include, url
from views import *
from opds.feeds import *

urlpatterns = patterns('/opds',
    url(r'^$', MainMenuFeed()),
    url(r'^search-genre/$', GenreCharsFeed()),
    url(r'^search-genre/(?P<char_id>\d+)/$', GenresByCharFeed()),
    url(r'^genre/(?P<genre_id>\d+)/$', BookByGenreFeed()),
    url(r'^search-author/$', AuthorCharsFeed()),
    url(r'^search-author/(?P<char_id>\d+)/$', AuthorsByCharFeed()),
    url(r'^author/(?P<author_id>\d+)/$', BookByAuthorFeed()),
)