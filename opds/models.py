# -*- coding: utf-8 -*-
from django.db import models


class Char(models.Model):
    """ Char. Search optimisation """
    char = models.CharField(u"Char", max_length=3)

    def get_absolute_url(self):
        return '/opds/authors/%s' % self.id

    def __unicode__(self):
        return u'/opds/autors/%s - Authors on %s' % (self.char, self.char)


class MenuItem(models.Model):
    """ Main menu items for OPDS feed """
    title = models.CharField(u"Title", max_length=300, null=True, blank=True)
    link = models.CharField(u"Link", max_length=400, null=True, blank=True)
    description = models.TextField(u"Description", null=True, blank=True)
    group = models.CharField(u"Group", max_length=40, null=True, blank=True)
    order = models.IntegerField(u"Order", default=0)

    def get_absolute_url(self):
        return '/opds/%s/' % self.link

    def __unicode__(self):
        return '/opds/%s - %s' % (self.link,self.title)