# -*- coding: utf-8 -*-
from django.db import models

from fb2lib.settings import FILE_SERVER, IMAGE_SERVER


class Language(models.Model):
    """ Язык книги """
    code = models.CharField(u'Код языка', max_length=50, null=False)
    name = models.CharField(u'Название', max_length=100, null=True)

    class Meta:
        verbose_name = u'Язык'
        verbose_name_plural = u'Языки'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)


class Publisher(models.Model):
    """ Издатель """
    name = models.CharField(u'Название издательства', max_length=150)
    city = models.CharField(u'Город', max_length=100, null=True, blank=True)
    website = models.URLField(u'Адрес сайта', null=True, blank=True)
    year = models.CharField(u'Год', max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = u'Издатель'
        verbose_name_plural = u'Издатели'

    def __unicode__(self):
        return self.name


class Genre(models.Model):
    """ Жанр книги """
    code = models.CharField(u'Код жанра', max_length=50)
    name = models.CharField(u'Название жанра', max_length=300, null=True,
                            blank=True)

    class Meta:
        verbose_name = u'Жанр'
        verbose_name_plural = u'Жанры'

    def __unicode__(self):
        return self.name

    def get_absolute_url_opds(self):
        return "/opds/genre/%d" % self.id


class Sequence(models.Model):
    """ Серии """
    name = models.CharField(u'Название серии', max_length=300)

    class Meta:
        verbose_name = u'Серия'
        verbose_name_plural = u'Серии'

    def __unicode__(self):
        return self.name

    def get_absolute_url_opds(self):
        return "/opds/sequence/%d/" % self.id


class Author(models.Model):
    """ Автор """
    first_name = models.CharField(u'Имя', max_length=200, default='000')
    middle_name = models.CharField(u'Отчество', max_length=200, null=True,
                                   blank=True)
    last_name = models.CharField(u'Фамилия', max_length=200, default='000')

    class Meta:
        verbose_name = u'Автор'
        verbose_name_plural = u'Авторы'

    def __unicode__(self):
        return self.last_name + ' ' + self.first_name

    def get_absolute_url_opds(self):
        return "/opds/author/%d/" % self.id

    def get_absolute_url(self):
        return "/book/author/%d/" % self.id


class Translator(Author):
    """ Переводчик """

    class Meta:
        verbose_name = u'Переводчик'
        verbose_name_plural = u'Переводчики'


class SequenceBook(models.Model):
    """ Расшивка серия-книга"""
    book = models.ForeignKey('Book', verbose_name=u'Книга', null=True,
                             blank=True)
    number = models.CharField(u'Номер в серии', null=True, blank=True,
                              max_length=10)
    sequence = models.ForeignKey('Sequence', verbose_name=u'Жанр', null=True,
                                 blank=True)

    class Meta:
        verbose_name = u'Серия книги'
        verbose_name_plural = u'Серии книг'

    def __unicode__(self):
        return "%s - %s (%s)" % (self.book.title,
                                 self.sequence.name,
                                 self.number)


class Book(models.Model):
    """ Книга """
    title = models.CharField(u'Название', max_length=300)
    genre = models.ManyToManyField(Genre, verbose_name=u'Жанры', null=True)
    annotation = models.TextField(u'Описание', null=True, blank=True)
    authors = models.ManyToManyField(Author, verbose_name=u'Авторы',
                                     related_name='books')
    lang = models.ForeignKey(Language, verbose_name=u'Язык', null=True,
                             related_name=u'book_lang')
    src_lang = models.ForeignKey(Language, verbose_name=u'Язык оригинала',
                                 null=True, related_name=u'book_src_lang')
    date = models.CharField(u'Дата', max_length=50, null=True, blank=True)
    sequence = models.ManyToManyField('Sequence', verbose_name=u'Серии книги',
                                      null=True, through='SequenceBook')
    book_file = models.CharField(u'Файл', max_length=1000)
    image = models.ImageField(u'Обложка', upload_to='covers/', null=True,
                              blank=True, max_length=300)
    md5 = models.CharField(u'Hash', max_length=150, default='000')
    publisher = models.ManyToManyField(Publisher, verbose_name=u'Издатель',
                                       null=True)
    translator = models.ManyToManyField(Translator, related_name='translators',
                                        verbose_name=u'Переводчик', null=True)
    uuid = models.CharField(u"UUID", max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = u'Книга'
        verbose_name_plural = u'Книги'

    def add_sequences(self, sequence_list):
        for _seq, num in sequence_list:
            try:
                num = int(num)
            except (ValueError, TypeError), e:
                print e
                num = None
            if not num and not SequenceBook.objects.filter(book=self,
                                                           sequence=_seq,
                                                           number=num).exists():
                SequenceBook.objects.create(
                    book=self,
                    sequence=_seq,
                    number=num
                )
            else:
                SequenceBook.objects.create(
                    book=self,
                    sequence=_seq,
                )

    def __unicode__(self):
        return self.title

    def get_absolute_url_opds(self):
        return "/opds/book/%d/" % self.id

    def get_absolute_url(self):
        return "/book/%d/" % self.id

    def get_cover_url(self):
        return IMAGE_SERVER + '/' + self.image.url

    def get_download_url(self):
        return FILE_SERVER + '/' + self.book_file.replace("\\", "/")

    def get_authors_string(self):
        authors = self.authors.all()
        return ", ".join([
            "%s %s" % (author.last_name, author.first_name)
            for author in authors])



