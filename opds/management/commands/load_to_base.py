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
        self.load_to_base()

    def load_to_base(self):
        """ Функция пробегает по каталогам, считывает книги и сохраняет их в дереве LIB_PATH """
        # пробегаем по дереву каталогов
        log = open(PATH + 'log_db.txt', 'w')
        log.write('\n')
        print "Looking in: " + PATH
        bookcount = 0
        start = datetime.datetime.now()
        for (dirname, subshere, fileshere) in os.walk(PATH):
            if len(dirname.split('utf-8')[1])>1 and dirname.split('utf-8')[1][1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                print dirname.split('utf-8')[1][1]
                continue
            book_file = None
            for fname in fileshere:
                if fname.split('.')[-1] == 'fb2':
                    book_file = fname
                if book_file:
                    f = open(os.path.join(dirname, book_file), 'r')
                    book_string = f.read()
                    f.close()
                    # В случае завала скрипта по хешам смотрим, читали эту книгу или не читали
                    if not Book.objects.filter(md5=hashlib.md5(book_string).hexdigest()).exists():
                        book = FBook(book_string)
                        if book._broken:
                            log.write(os.path.join(dirname, book_file) + '\n')
                            continue
                        print 'Book: %s' % book_file
                        if Genre.objects.filter(code=book.title_info['genre']).exists():
                            genre = Genre.objects.filter(code=book.title_info['genre'])[0]
                        else:
                            genre = Genre.objects.create(code=book.title_info['genre'])
                        sequences = []
                        if book.title_info['sequence']:
                            for _seq in book.title_info['sequence']:
                                sequence = None
                                if 'name' in _seq:
                                    if Sequence.objects.filter(name=_seq['name']).exists():
                                        sequence = Sequence.objects.filter(name=_seq['name'])[0]
                                    else:
                                        sequence = Sequence.objects.create(name=_seq['name'])
                                if sequence:
                                    sequences.append((sequence, _seq['number'] if 'number' in _seq else None))
                        authors = []
                        for a_tuple in book.title_info['authors']:
                            if Author.objects.filter(first_name=a_tuple[0], middle_name=a_tuple[1], last_name=a_tuple[2]).exists():
                                author = Author.objects.filter(first_name=a_tuple[0], middle_name=a_tuple[1], last_name=a_tuple[2])[0]
                            else:
                                author = Author.objects.create(first_name=a_tuple[0], middle_name=a_tuple[1], last_name=a_tuple[2])
                            if author:
                                authors.append(author)
                        fbook = Book.objects.create(
                            title=book.title_info['book-title'],
                            genre=genre,
                            annotation=book.title_info['annotation'],
                            lang=book.title_info['lang'],
                            book_file=os.path.join(dirname, book_file),
                            md5=hashlib.md5(book_string).hexdigest()
                        )
                        if 'data' in book.title_info['coverpage']:
                            image_data = b64decode(book.title_info['coverpage']['data'])
                            fbook.image = ContentFile(image_data, fbook.md5 + '.' + book.title_info['coverpage']['ext'])
                            fbook.save()
                        if sequences:
                            fbook.add_sequences(sequences)
                        if authors:
                            fbook.authors.add(*authors)

                        fbook.save()
                        bookcount +=1
                        if bookcount % 50 == 0:
                            f = open('/media/library/stat.log', 'a')
                            now = datetime.datetime.now()
                            f.write('Book loaded: %d    Time: %s\n' % (bookcount, now-start))
                            f.close()
