# -*- coding: utf-8 -*-
import os
from base64 import b64decode
import hashlib
import datetime
from django.core.management.base import NoArgsCommand
from django.core.files.base import ContentFile


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.filter_language()

    def filter_language(self):
        """ Remove models.Language duplicates """
        # todo
        pass
