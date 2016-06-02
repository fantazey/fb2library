# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.contrib.sites.models import Site
from django.core import serializers
from book.models import *
from opds.models import *


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.load_data()

    def load_data(self):
        """ Генерирует объекты main.Char на основе таблицы авторов """
        # todo
        pass
