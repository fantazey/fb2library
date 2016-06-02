# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from book.models import *


def get_menu_data():
    all_letters = []
    for x in Author.objects.all().order_by('last_name').\
            values_list('last_name', flat=True):
        if len(x) > 0:
            all_letters.append(x[0])
    letters = []
    for letter in all_letters:
        if not letter.upper() in letters:
            letters.append(letter.upper())
    letters = sorted(letters)
    genres = Genre.objects.filter(name__isnull=False).order_by('name')
    genres = [
        {
            'id': genre.id,
            'name': genre.name,
            'count': genre.book_set.count()
        } for genre in genres]
    return letters, genres


def index(request):
    """ Главная страница """
    letters, genres = get_menu_data()
    last_books = Book.objects.all().order_by('-id')[:20]
    return render_to_response(
        'main/index.html',
        {
            'letters': letters,
            'last_books': last_books,
            'genres': genres,
        },
        context_instance=RequestContext(request))
