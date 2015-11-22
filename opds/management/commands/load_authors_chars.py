# -*- coding: utf-8 -*-
__author__ = 'Andrew'


from django.core.management.base import NoArgsCommand
from opds.models import Char
from book.models import Author


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.load_authors_chars()

    def load_authors_chars(self):
        authors = Author.objects.all().values_list('last_name', flat=True)
        for a in authors:
            if len(a) > 0 and not Char.objects.filter(char=a[0]).exists():
                Char.objects.create(char=a[0])
