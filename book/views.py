# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from book.models import *
from main.views import get_menu_data
from opds.models import Char
from battaries.decorators import render_to


def library(request):
    return render_to_response('main/__index.html', {}, context_instance=RequestContext(request))

@render_to("book/letters.html")
def letters(request):
    """
    Вывести список букв для поиска автора
    """
    title = u"Выберите первую букву фамилии автора"
    return {
        'letters': Char.objects.all().order_by('char'),
        'title': title
    }


@render_to("book/genres.html")
def genres(request):
    genre_list = Genre.objects.all().order_by('name')
    paginator = Paginator(genre_list, 10)
    page = request.GET.get("page", 1)
    try:
        _genres = paginator.page(page)
    except EmptyPage:
        _genres = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        _genres = paginator.page(1)
    return {
        'genres': _genres
    }


@render_to("book/sequences.html")
def sequences(request):
    sequence_list = Sequence.objects.all().order_by('name')
    paginator = Paginator(sequence_list, 10)
    page = request.GET.get("page", 1)
    try:
        _sequences = paginator.page(page)
    except EmptyPage:
        _sequences = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        _sequences = paginator.page(1)
    return {
        'sequences': _sequences
    }


@render_to("book/authors_letter.html")
def author_letter(request, letter):
    """
    Авторы с фамилией на букву letter
    """
    title = u"Авторы с фамилиями на букву %s" % letter
    if len(letter) != 1:
        raise Http404
    all_authors = Author.objects.filter(
        Q(last_name__startswith=letter.upper()) |
        Q(last_name__startswith=letter.lower())
    )
    all_authors = all_authors.order_by('last_name')
    paginator = Paginator(all_authors, 60)
    page = request.GET.get("page", 1)
    try:
        authors = paginator.page(page)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        authors = paginator.page(1)
    return {
        'authors': authors,
        'title': title
    }



@render_to("book/book_details.html")
def book_details(request, book_id):
    """
    Подробнее о книге
    """
    book = Book.objects.get(id=book_id)
    sequences = []
    genres = Genre.objects.filter(name__isnull=False).order_by('name')
    genres = [
        {'id': genre.id,
         'name': genre.name,
         'count': genre.book_set.count()} for genre in genres
    ]
    for sequence in book.sequence.all():
        sequences.append({
            'name': sequence.name,
            'number': SequenceBook.objects.get(book=book,sequence=sequence).number ,
            'id': sequence.id,
        })
    letters, genres = get_menu_data()
    return {
            'book': book,
            'sequences': sequences,
            'genres': genres,
            'letters': letters
    }

def genre_books(request, id):
    """
    Книги жанра
    """
    all_books = Book.objects.filter(genre__id=id).order_by('title')
    paginator = Paginator(all_books, 50)
    page = request.GET.get("page", 1)
    try:
        books = paginator.page(page)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        books = paginator.page(1)
    letters, genres = get_menu_data()
    return render_to_response(
        'book/author_books.html',
        {
            'books': books,
            'genres': genres,
            'letters': letters
        },
        context_instance=RequestContext(request))


@render_to("book/author_books.html")
def author_books(request, author_id):
    """
    Книги автора
    """
    author = Author.objects.get(id=author_id)
    title = u"Книги автора: %s" % author.__unicode__()
    all_books = author.books.all().order_by('title')
    paginator = Paginator(all_books, 50)
    page = request.GET.get("page", 1)
    try:
        books = paginator.page(page)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        books = paginator.page(1)
    return {
        'books': books,
        'title': title
    }
