from django import template
from django.conf import settings

register = template.Library()


def rebase_url(value, empty=False):
    """Removes all values of arg from the given string"""
    if not empty:
        return settings.IMAGE_SERVER + value
    else:
        return settings.IMAGE_SERVER + '/static/img/empty_cover.jpg'
register.filter('rebase_url', rebase_url)