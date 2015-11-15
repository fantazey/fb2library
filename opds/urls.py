__author__ = 'Andrew'

from django.conf.urls import patterns, url
from opds.feeds import *

urlpatterns = patterns('/opds',
    url(r'^main/$', TestMainFeed()),
    url(r'^authors/$', TestAutorsFeed()),
    url(r'^authors/(?P<char_id>\d+)/$', TestAutorsCharFeed()),
    url(r'^author/(?P<author_id>\d+)/$', TestAuthorFeed())
)