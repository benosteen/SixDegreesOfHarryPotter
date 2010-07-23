#!/usr/bin/env python

from redis import Redis
from talis_isbn import ISBNAPI
from openlibrary import OLAPI

class SixDegrees(object):
    """Key guide:
        h - set of harry potter isbns
        r{level} - set of related potter books at {level}
        lvls - set of levels populated"""
    def __init__(self, **kw):
        self.kw = kw
        self.r = Redis(**self.kw)

    def talis_appearswith(self, isbn, cache_update = False):
        if not cache_update:
            searched = self.r.get("talis:appearswith:%s" % isbn)
            cached = self.r.smembers("ct:isbn:%s" % isbn)
            if searched: return cached
        i = ISBNAPI()
        data = i.appearswith(isbn=isbn)
        records = data['recommendations']
        self.r.set("talis:appearswith:%s" % isbn, 1)
        if records:
            related_books = []
            for record in records:
                if record['id'].startswith("isbn/"):
                    related_books.append(record['id'][5:])
                    self.r.sadd("ct:isbn:%s" % isbn, record['id'][5:])
            return related_books

    def ol_lookup_isbn_10(self, isbn, params_to_return=['title','subjects']):
        ol = OLAPI()
        r_keys = dict( [(x, "") for x in params_to_return] )
        return ol.query(isbn_10=isbn, **r_keys)

    def load_potter_isbns(self, books):
        for book in books:
            self.add_potter_book(book, books[book])

    def add_potter_book(self, isbn, title=None):
        self.r.sadd("h", isbn)
        if title:
            self.r.set("isbn:%s" % isbn, title) # isbn --> "title"

    def get_title(self, isbn):
        return self.r.get("isbn:%s" % isbn)

    def list_potter_isbns(self):
        return self.r.smembers("h")
 
    def get_related(self, level):
        return self.r.smembers("r%s" % level)

    def talis_populate_level_up(self, base_level):
        next_level = int(base_level) + 1
        seeds = self.get_related(base_level)
        n_level = []
        for isbn in seeds:
            resp = self.talis_appearswith(isbn)
            if resp:
                n_level.extend(resp)
        self.addrelated(next_level, n_level)
        return self.get_related(next_level)

    def addrelated(self, level, isbns):
        for item in isbns:
            try:
                self.r.sadd("r%s" % level, item)
                if isinstance(isbns, dict):
                    self.r.set("isbn:%s" % item, isbns[item])
                self.r.sadd("lvls", level)
            except: # SocketError of some sort
                self.r = Redis(**self.kw)
                self.r.sadd("r%s" % level, item) 
                if isinstance(isbns, dict):
                    self.r.set("isbn:%s" % item, isbns[item])
                self.r.sadd("lvls", level)

    def isthisrelated(self, isbn):
        for level in self.r.smembers("lvls"):
            if self.r.sismember("r%s" % level, isbn):
                return level
