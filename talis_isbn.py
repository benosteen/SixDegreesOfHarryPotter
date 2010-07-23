#!/usr/bin/env python

from httplib2 import Http
from urllib import urlencode

import simplejson

class ISBNAPI(object):
    def __init__(self, url_base="http://prototype.talisaspire.com/isbn/%(isbn)s/%(verb)s"):
        self.h = Http()
        self.b = url_base

    def appearswith(self, **kw):
        if not kw.has_key("isbn"):
            raise Exception("Must supply an isbn parameter")
        else:
            rest = {'isbn':kw['isbn']}
        rest['verb'] = "appears-with"
        count = kw.get("count", 25)
        (resp, content) = self.h.request("?".join([self.b % (rest),"count=%s&api_key=hackday" % count]))
        try: 
            payload = simplejson.loads(content)
            return payload
        except simplejson.decoder.JSONDecodeError:
            print "Got unintelligible response from Talis Server"
            print resp
            print "-"*30
            print content
            print "-"*30
            return {'recommendations':[]}
