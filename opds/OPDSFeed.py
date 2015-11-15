# -*- coding: utf-8 -*-
__author__ = 'andrew'
__all__ = ['NaviFeed', 'BookFeed']

from django.utils.feedgenerator import Atom1Feed, rfc3339_date, get_tag_uri
from datetime import datetime
# Модуль для реализации классов OPDS Feed на основе Django Syndication Framework


class NaviFeed(Atom1Feed):

    mime_type = 'application/atom+xml; charset=utf-8'
    ns = "http://www.w3.org/2005/Atom"
    link_type = "application/atom+xml;profile=opds-catalog;kind=navigation"

    def __init__(self, *args, **kwargs):
        super(NaviFeed, self).__init__(*args, **kwargs)
        self.feed['start_link'] = '/opds/main'

    def add_root_elements(self, handler):
        handler.addQuickElement(
            "title",
            self.feed['title']
        )
        handler.addQuickElement(
            "link",
            "",
            {
                "rel": "start",
                "href": self.feed['start_link'],
                "type": self.link_type
            }
        )
        if self.feed['feed_url'] is not None:
            handler.addQuickElement(
                "link",
                "",
                {
                    "rel": "self",
                    "href": self.feed['feed_url'],
                    "type": self.link_type
                }
            )
        handler.addQuickElement("id", self.feed['id'])
        handler.addQuickElement(
            "updated",
            rfc3339_date(self.latest_post_date())
        )
        if self.feed['author_name'] is not None:
            handler.startElement("author", {})
            handler.addQuickElement("name", self.feed['author_name'])
            if self.feed['author_email'] is not None:
                handler.addQuickElement("email", self.feed['author_email'])
            if self.feed['author_link'] is not None:
                handler.addQuickElement("uri", self.feed['author_link'])
            handler.endElement("author")

    def add_item_elements(self, handler, item):
        handler.addQuickElement("title", item['title'])
        handler.addQuickElement(
            "updated",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        handler.addQuickElement(
            "link",
            "",
            {
                "href": item['link'],
                "type": self.link_type
            }
        )

        if item['unique_id'] is not None:
            unique_id = item['unique_id']
        else:
            unique_id = get_tag_uri(item['link'], item['pubdate'])
        handler.addQuickElement("id", unique_id)
        handler.addQuickElement(
            "content",
            item['description'],
            attrs={
                "type": "text"
            }
        )


class BookFeed(NaviFeed):
    ac_link_type = "application/atom+xml;profile=opds-catalog;kind=acquisition"
    mime_type = 'application/atom+xml; charset=utf-8'
    ns = "http://www.w3.org/2005/Atom"

    def __init__(self, *args, **kwargs):
        super(BookFeed, self).__init__(*args, **kwargs)

    def add_item_elements(self, handler, item):
        handler.addQuickElement("title", item['title'])
        handler.addQuickElement(
            "updated",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        handler.addQuickElement(
            "link",
            "",
            {
                "href": item['link'],
                "type": self.ac_link_type
            }
        )
        if item['unique_id'] is not None:
            unique_id = item['unique_id']
        else:
            unique_id = get_tag_uri(item['link'], item['pubdate'])
        handler.addQuickElement("id", unique_id)
        handler.addQuickElement(
            "category",
            "",
            {
                "label": item['category_label'],
                "term": item['category_term'],
                "scheme": "http://www.fictionbook.org/index.php/%D0%96%D0%B0%D0%BD%D1%80%D1%8B_FictionBook_2.1/"
            }
        )
        handler.addQuickElement(
            "link",
            "",
            {
                "type": "text/html",
                "href": item['abs_link'],
                "rel": "alternate",
                "title": item['title']
            }
        )
        handler.addQuickElement(
            "link",
            "",
            {
                "type": "image/jpeg",
                "href": item['cover_link'],
                "rel": "http://opds-spec.org/image",
            }
        )
        handler.addQuickElement(
            "link",
            "",
            {
                "type": "image/jpeg",
                "href": item['cover_thumb_link'],
                "rel": "http://opds-spec.org/image/thumbnail",
            }
        )
        handler.addQuickElement(
            "link",
            "",
            {
                "type": "application/fb2+zip",
                "href": item['download_link'],
                "rel": "http://opds-spec.org/acquisition",
                "title": item['title']
            }
        )