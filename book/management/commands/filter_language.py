# -*- coding: utf-8 -*-
__author__ = 'andy'

import os
from base64 import b64decode
import hashlib
import datetime
from django.core.management.base import NoArgsCommand
from django.core.files.base import ContentFile

from book.fb2 import FBook, SAVE_PATH
from book.models import *

PATH = '/media/library/utf-8/'
# В какой каталог складывать нераспознанные
PATH_UNSORTED = SAVE_PATH + '/media/library/Unsorted/'


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.filter_language()

    def filter_language(self):
        """ Убить дубликаты models.Language """
        pass