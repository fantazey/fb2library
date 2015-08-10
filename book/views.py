# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from book.models import *
from main.views import get_menu_data

def library(request):
    return render_to_response('main/__index.html', {}, context_instance=RequestContext(request))

def book_details(request, id):
    """
    Подробнее о книге
    """
    book = Book.objects.get(id=id)
    sequences = []
    genres = Genre.objects.filter(name__isnull=False).order_by('name')
    genres = [{'id': genre.id, 'name': genre.name, 'count': genre.book_set.count()} for genre in genres]
    for sequence in book.sequence.all():
        sequences.append({
            'name': sequence.name,
            'number': SequenceBook.objects.get(book=book,sequence=sequence).number ,
            'id': sequence.id,
        })
    letters, genres = get_menu_data()
    return render_to_response(
        'book/book_details.html',
        {
            'book': book,
            'sequences': sequences,
            'genres': genres,
            'letters': letters
        },
        context_instance=RequestContext(request))

def author_letter(request, letter):
    """
    Авторы с фамилией на букву letter
    """
    if len(letter) != 1:
        raise Http404
    all_authors = Author.objects.filter(Q(last_name__startswith=letter.upper()) | Q(last_name__startswith=letter.lower()))
    all_authors = all_authors.order_by('last_name')
    paginator = Paginator(all_authors, 60)
    page = request.GET.get("page", 1)
    try:
        authors = paginator.page(page)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        authors = paginator.page(1)
    letters, genres = get_menu_data()
    return render_to_response(
        'book/authors_letter.html',
        {
            'authors': authors,
            'genres': genres,
            'letters': letters
        },
        context_instance=RequestContext(request))

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
        'book/books_list.html',
        {
            'books': books,
            'genres': genres,
            'letters': letters
        },
        context_instance=RequestContext(request))

def author_books(request, id):
    """
    Книги автора
    """
    all_books = Author.objects.get(id=id).book_set.all().order_by('title')
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
        'book/books_list.html',
        {
            'books': books,
            'genres': genres,
            'letters': letters
        },
        context_instance=RequestContext(request))
