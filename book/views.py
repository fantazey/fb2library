# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.db.models import Q
from django.http import Http404
from book.models import *
from opds.models import Char
from battaries.decorators import render_to


def library(request):
    return render_to_response(
        'main/__index.html',
        {},
        context_instance=RequestContext(request)
    )


@render_to("book/letters.html")
def letters(request):
    """
    Show list of letters
    """
    title = u"choose first char of last-name"
    return {
        'letters': Char.objects.all().order_by('char'),
        'title': title
    }


@render_to("book/genres.html")
def genres(request):
    title = u"List of genres"
    return {
        'genres': Genre.objects.all().order_by('name'),
        'title': title
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
    Authors whom last-names startswith letter
    """
    title = u"Authors whom last-names startswith %s" % letter
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
    title = u"Book"
    book = Book.objects.get(id=book_id)
    return {
        'book': book,
        'title': title
    }


@render_to('book/author_books.html')
def genre_books(request, genre_id):
    """
    Books with genre genre_id
    """
    all_books = Book.objects.filter(genre__id=genre_id).order_by('title')
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
        'genres': genres,
        'letters': letters
    }


@render_to("book/author_books.html")
def author_books(request, author_id):
    """
    Books of author author_id
    """
    author = Author.objects.get(id=author_id)
    title = u"Books of author: %s" % author.__unicode__()
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
