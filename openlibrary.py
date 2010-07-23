#!/usr/bin/env python

from httplib2 import Http
from urllib import urlencode

import simplejson

class OLAPI(object):
    def __init__(self, url_base="http://openlibrary.org/query.json"):
        self.h = Http()
        self.b = url_base

    def query(self, qtype="/type/edition", **kw):
        kw['type'] = qtype
        params = urlencode(kw)
        
        (resp, content) = self.h.request("?".join([self.b,params]) )
        try: 
            payload = simplejson.loads(content)
            return payload
        except simplejson.decoder.JSONDecodeError:
            print "Got unintelligible response from OpenLibrary Server"
            print resp
            print "-"*30
            print content
            print "-"*30
