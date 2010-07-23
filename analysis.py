from sixdegrees import SixDegrees

s = SixDegrees()

# Go through each level and get titles and subjects for as many of the ISBNs as possible using the Open Library API

for level in [1,2,3,4,5,6,7]:
    isbns = s.get_related(level)
    for isbn in isbns:
        results = s.ol_lookup_isbn_10(isbn)
        # Lazy - assume first result is most relevant
        if results:
            result = results[0]
            s.r.incr("tally:%s" % level)
            s.r.set("isbn:%s" % isbn, result.get("title") )
            print result.get("title")
            subjs = result.get("subjects", [])
            if subjs:
                for subj in subjs:
                    print subj
                    s.r.sadd("subj:%s" % level, subj)
        else:
            s.r.incr("misses:%s" % level)
for level in [1,2,3,4,5,6,7]:
    print "Level %s" % level
    print "Sample Titles:"
    for isbn in s.get_related(level):
        if s.r.get("isbn:%s" % isbn):
            print s.r.get("isbn:%s" % isbn)
    print "Subject areas:"
    print "Number of subjects: %s" % s.r.scard("subj:%s" % level)
    print ", ".join(s.r.smembers("subj:%s" % level))
    print "Couldn't look up %s %% of the ISBNs" % ( float(s.r.get("misses:%s" % level)) / float(s.r.scard("r%s" % level)) * 100.0  )

