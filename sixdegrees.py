#!/usr/bin/env python

from redis import Redis
from talis_isbn import ISBNAPI

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
            cached = self.r.smembers("ct:isbn:%s" % isbn)
            if cached: return cached
        i = ISBNAPI()
        data = i.appearswith(isbn=isbn)
        records = data['recommendations']
        if records:
            related_books = []
            for record in records:
                if record['id'].startswith("isbn/"):
                    related_books.append(record['id'][5:])
                    self.r.sadd("ct:isbn:%s" % isbn, record['id'][5:])
            return related_books

    def load_potter_isbns(self, books):
        for book in books:
            self.r.sadd("h", book)
            self.r.set("isbn:%s" % book, books[book]) # isbn --> "title"

    def list_potter_isbns(self):
        return self.r.smembers("h")

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
