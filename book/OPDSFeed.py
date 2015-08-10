__author__ = 'andrew'
from django.utils.feedgenerator import Atom1Feed, SyndicationFeed, rfc3339_date, get_tag_uri


class OPDS(Atom1Feed):
    mime_type = 'application/atom+xml; charset=utf-8'
    ns = "http://www.w3.org/2005/Atom"

    def __init__(self, alt_link=None, *args, **kwargs):
        super(OPDS, self).__init__(*args, **kwargs)
        self.feed['alt_link'] = alt_link


    def add_root_elements(self, handler):
        handler.addQuickElement("title", self.feed['title'])
        handler.addQuickElement("link", "", {"rel": "alternate", "href": self.feed['alt_link'], "type": self.feed['alt_link_type']})
        if self.feed['feed_url'] is not None:
            handler.addQuickElement("link", "", {"rel": "self", "href": self.feed['feed_url'], "type": self.feed['self_link_type']})
        handler.addQuickElement("id", self.feed['id'])
        handler.addQuickElement("updated", rfc3339_date(self.latest_post_date()))
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
        handler.addQuickElement("link", "", {
            "href": item['link'],
            "rel": "alternate",
            "type": "application/atom+xml;profile=opds-catalog;kind=acquisition"
        })

        # Unique ID.
        if item['unique_id'] is not None:
            unique_id = item['unique_id']
        else:
            unique_id = get_tag_uri(item['link'], item['pubdate'])
        handler.addQuickElement("id", unique_id)
        handler.addQuickElement("content", item["content"], attrs={"type": "text"})