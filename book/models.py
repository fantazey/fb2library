# -*- coding: utf-8 -*-
from django.db import models

from fb2lib.settings import FILE_SERVER, IMAGE_SERVER


class Language(models.Model):
    """ Book language """
    code = models.CharField(u'Language code', max_length=50, null=False)
    name = models.CharField(u'Name', max_length=100, null=True)

    class Meta:
        verbose_name = u'Language'
        verbose_name_plural = u'Languages'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.code)


class Publisher(models.Model):
    """ Book publisher """
    name = models.CharField(u'Name', max_length=150)
    city = models.CharField(u'City', max_length=100, null=True, blank=True)
    website = models.URLField(u'Web-Site', null=True, blank=True)
    year = models.CharField(u'Year', max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = u'Publisher'
        verbose_name_plural = u'Publishers'

    def __unicode__(self):
        return self.name


class Genre(models.Model):
    """ Book genre """
    code = models.CharField(u'Genre code', max_length=50)
    name = models.CharField(u'Name', max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = u'Genre'
        verbose_name_plural = u'Genres'

    def __unicode__(self):
        return self.name

    def get_absolute_url_opds(self):
        return "/opds/genre/%d" % self.id

    def get_absolute_url(self):
        return "/book/genre/%d" % self.id


class Sequence(models.Model):
    """ Sequence """
    name = models.CharField(u'Name', max_length=300)

    class Meta:
        verbose_name = u'Sequence'
        verbose_name_plural = u'Sequences'

    def __unicode__(self):
        return self.name

    def get_absolute_url_opds(self):
        return "/opds/sequence/%d/" % self.id


class Author(models.Model):
    """ Author """
    first_name = models.CharField(u'First name', max_length=200, default='000')
    middle_name = models.CharField(u'Middle name', max_length=200, null=True,
                                   blank=True)
    last_name = models.CharField(u'Last name', max_length=200, default='000')

    class Meta:
        verbose_name = u'Author'
        verbose_name_plural = u'Authors'

    def __unicode__(self):
        return self.last_name + ' ' + self.first_name

    def get_absolute_url_opds(self):
        return "/opds/author/%d/" % self.id

    def get_absolute_url(self):
        return "/book/author/%d/" % self.id


class Translator(Author):
    """ Translator """

    class Meta:
        verbose_name = u'Translator'
        verbose_name_plural = u'Translators'


class SequenceBook(models.Model):
    """ Book from sequence """
    book = models.ForeignKey('Book', verbose_name=u'Book', null=True,
                             blank=True)
    number = models.CharField(u'Number in sequence', null=True, blank=True,
                              max_length=10)
    sequence = models.ForeignKey('Sequence', verbose_name=u'Sequence',
                                 null=True, blank=True)

    class Meta:
        verbose_name = u'Book sequence'
        verbose_name_plural = u'Books sequence'

    def __unicode__(self):
        return "%s - %s (%s)" % (self.book.title,
                                 self.sequence.name,
                                 self.number)


class Book(models.Model):
    """ Книга """
    title = models.CharField(u'Title', max_length=300)
    genre = models.ManyToManyField(Genre, verbose_name=u'Genres', null=True,
                                   related_name='books')
    annotation = models.TextField(u'Annotation', null=True, blank=True)
    authors = models.ManyToManyField(Author, verbose_name=u'Authors',
                                     related_name='books')
    lang = models.ForeignKey(Language, verbose_name=u'Language', null=True,
                             related_name=u'book_lang')
    src_lang = models.ForeignKey(Language, verbose_name=u'Original language',
                                 null=True, related_name=u'book_src_lang')
    date = models.CharField(u'Date', max_length=50, null=True, blank=True)
    sequence = models.ManyToManyField('Sequence', verbose_name=u'Sequences',
                                      null=True, through='SequenceBook')
    book_file = models.CharField(u'File', max_length=1000)
    image = models.ImageField(u'Cover', upload_to='covers/', null=True,
                              blank=True, max_length=300)
    md5 = models.CharField(u'Hash', max_length=150, default='000')
    publisher = models.ManyToManyField(Publisher, verbose_name=u'Publisher',
                                       null=True)
    translator = models.ManyToManyField(Translator, related_name='translators',
                                        verbose_name=u'Translator', null=True)
    uuid = models.CharField(u"UUID", max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = u'Book'
        verbose_name_plural = u'Books'

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



