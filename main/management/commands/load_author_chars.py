# -*- coding: utf-8 -*-
__author__ = 'andy'

from django.core.management.base import NoArgsCommand
from book.models import Author
from main.models import Char


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.load_authors_chars()

    def load_authors_chars(self):
        """ Генерирует объекты main.Char на основе таблицы авторов """
        autors = Author.objects.all().values_list('last_name', flat=True)
        for autor in autors:
            if not Char.objects.filter(char=autor[0]).exists():
                Char.objects.create(char=autor[0])