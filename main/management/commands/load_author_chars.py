# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from book.models import Author
from opds.models import Char


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.load_authors_chars()

    def load_authors_chars(self):
        """ Генерирует объекты main.Char на основе таблицы авторов """
        authors = Author.objects.all().values_list('last_name', flat=True)
        for author in authors:
            if len(author) > 0 and \
                    not Char.objects.filter(char=author[0]).exists():
                Char.objects.create(char=author[0])
