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
    print "Row didn't have isbns"
    print openlib_row

with open("query.json", "r") as q_json:
    jdata = simplejson.loads(q_json.read())
    for record in jdata:
        isbns = get_isbn(record)
        if isbns:
            for i in isbns:
                s.add_potter_book(i, title=record.get('title'))

potters = s.list_potter_isbns()

r_books = []
for potter in potters:
    resp = s.talis_appearswith(potter)
    if resp:
        print "YES - ISBN %s -> Title: %s" % (potter, s.get_title(potter))
        r_books.extend(resp)
    else:
        pass
        # print "NO  - ISBN %s -> Title: %s" % (potter, s.get_title(potter))
print r_books
s.addrelated("1", r_books)

s.talis_populate_level_up("1")
s.talis_populate_level_up("2")
s.talis_populate_level_up("3")
s.talis_populate_level_up("4")
s.talis_populate_level_up("5")
s.talis_populate_level_up("6")

