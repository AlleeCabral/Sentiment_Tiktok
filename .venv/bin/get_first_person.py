#!/home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/.venv/bin/python3
# -*- coding: utf-8 -*-
"""
get_first_person.py

Usage: get_first_person "person name"

Search for the given name and print the best matching result.
"""

import sys

# Import the IMDbPY package.
try:
    import imdb
except ImportError:
    print('You need to install the IMDbPY package!')
    sys.exit(1)


if len(sys.argv) != 2:
    print('Only one argument is required:')
    print('  %s "person name"' % sys.argv[0])
    sys.exit(2)

name = sys.argv[1]


i = imdb.IMDb()

try:
    # Do the search, and get the results (a list of Person objects).
    results = i.search_person(name)
except imdb.IMDbError as e:
    print("Probably you're not connected to Internet.  Complete error report:")
    print(e)
    sys.exit(3)

if not results:
    print('No matches for "%s", sorry.' % name)
    sys.exit(0)

# Print only the first result.
print('    Best match for "%s"' % name)

# This is a Person instance.
person = results[0]

# So far the Person object only contains basic information like the
# name; retrieve main information:
i.update(person)

print(person.summary())
