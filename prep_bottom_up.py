from sixdegrees import SixDegrees

s = SixDegrees()

potters = s.list_potter_isbns()

r_books = []
for potter in potters:
    resp = s.talis_appearswith(potter)
    if resp:
        r_books.extend(resp)
    else:
        print "ISBN: %s got no related items" % potter
print r_books
