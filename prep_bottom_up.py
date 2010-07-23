from sixdegrees import SixDegrees

import simplejson

s = SixDegrees()

def get_isbn(openlib_row):
    isbn = openlib_row.get("isbn_10")
    if isbn:
        #clean up and return isbn(s)
        # Might be a list
        cleaned = []
        for i_string in isbn:
            # remove '-'s
            c_i = "".join(i_string.split("-"))
            cleaned.append(c_i)
        return cleaned
    else:
        isbn = openlib_row.get("isbn_13")
        if isbn:
            # Clean up and return isbn(s) (13)
            return isbn

with open("query.json", "r") as q_json:
    jdata = simplejson.loads(q_json.read())
    for record in jdata:
        isbns = get_isbn(record)
        for i in isbns:
            s.add_potter_book(i, title=record.get('title'))

potters = s.list_potter_isbns()

r_books = []
for potter in potters:
    resp = s.talis_appearswith(potter)
    print "ISBN %s -> Title: %s" % (potter, s.get_title(potter))
    if resp:
        print "ISBN: %s got a MATCH!" % potter
        r_books.extend(resp)
    else:
        print "ISBN: %s got no related items" % potter
print r_books
