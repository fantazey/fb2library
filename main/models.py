# -*- coding: utf-8 -*-
from django.db import models


class Char(models.Model):
    """ Буква файмилии автора. Для оптимизации навигации """
    char = models.CharField(u"Буква", max_length=3)
