# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *


class MenuItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(MenuItem, MenuItemAdmin)


class CharAdmin(admin.ModelAdmin):
    pass
admin.site.register(Char, CharAdmin)
