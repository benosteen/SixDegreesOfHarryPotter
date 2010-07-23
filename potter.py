books = {'3639025903':"Gender Portrayal in J.K. Rowling's Harry Potter and the Order of the Phoenix",
         '0615244491':"Harry Potter and the Order of the Court",
         '0439211158':"Harry Potter and the prisoner of Azkaban",
         '6130218338':"Harry Potter and the Order of the Phoenix",
         '0760842744':"Harry Potter and the sorcerer's stone",
         '0739360388':"Harry Potter and the Deathly Hallows",
         '0545029376':"Harry Potter and the deathly hallows",
         '0545010225':"Harry Potter and the deathly hallows",
         '074754624X':"Harry Potter and the goblet of fire",
         '1551923378':"Harry Potter and the goblet of fire",
         '0439139597':"Harry Potter and the goblet of fire",
         '0439139600':"Harry Potter and the goblet of fire",
         '0747589941':"Harry Potter and the philosopher's stone",
         '043935806X':"Harry Potter and the Order of the Phoenix",
         '0747569401':"Harry Potter and the order of the phoenix",
         '0439358078':"Harry Potter and the Order of the Phoenix",
         '0439784549':"Harry Potter and the Half-Blood Prince",
         '0747581088':"Harry Potter and the half-blood prince",
         '0439791324':"Harry Potter and the Half-Blood Prince",
         '0439064864':"Harry Potter and the Chamber of Secrets",
         '0747538492':"Harry Potter and the chamber of secrets",
         '0439064872':"Harry Potter and the Chamber of Secrets"}


def load_potter():
    from sixdegrees import SixDegrees
    s = SixDegrees()
    s.load_potter_isbns(books)
