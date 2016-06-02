# -*- coding: utf-8 -*-
__author__ = 'Andrew'

from django.core.management.base import NoArgsCommand
from book.models import *
from opds.models import *
from django.contrib.sites.models import Site
from django.core import serializers


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.dump_data()

    def dump_data(self):
        """ Генерирует объекты main.Char на основе таблицы авторов """
        json_serializer = serializers.get_serializer('json')
        json_dumper = json_serializer()
        _models = [
            (Author, 'authors'), (Book, 'book'), (Sequence, 'sequence'),
            (SequenceBook, 'sequencebook'), (Genre, 'genre'),
            (Language, 'language'), (Translator,'translator'), (Char, 'char'),
            (MenuItem, 'menuitem'), (Publisher, 'publisher'), (Site, 'site')
        ]

        for model, name in _models:
            with open('%s.json' % name, 'w') as out:
                json_dumper.serialize(model.objects.all(), stream=out)