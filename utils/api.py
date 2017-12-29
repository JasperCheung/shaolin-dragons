import requests
import json
import random

f = open("./.secret.txt", 'rU')
keys = json.loads(f.read())
f.close()

GIPHY_KEY = keys['giphy']

GIPHY_URL = ""
DATAMUSE_URL = "http://api.datamuse.com/words?"

# Read categories in categories file
with open('categories.txt') as f:
    CATEGORIES = f.readlines()
CATEGORIES = [c.strip() for c in CATEGORIES]

# Given a category, return a list of the words that Datamuse returns
def find_hyponyms(category):
    url = DATAMUSE_URL + 'md=p&rel_gen={}'.format(category)
    res = requests.get(url)
    words = res.json()
    return words

# Remove words that do not satisfy the following conditions:
# between 3 - 10 letters
# no spaces
# API score > 100
# a non-proper noun
def filter_words(words):
    words = [w for w in words if not ' ' in w['word']]
    words = [w for w in words if len(w['word']) > 2 and len(w['word']) < 11 \
            and w['score'] > 100]
    words = [w for w in words if 'n' in w['tags'] and not 'prop' in w['tags']]
    return words

# Return a random hyponym given the list of filtered words
def random_word(words):
    return random.choice(words)['word']

if __name__ == "__main__":
    print(CATEGORIES)
    cat0 = filter_words(find_hyponyms(CATEGORIES[0]))
    cat1 = filter_words(find_hyponyms(CATEGORIES[1]))
    print len(cat0)
    print len(cat1)
    # for w in cat0:
    #     print w['word']
    for i in range(5):
        print "0: " + random_word(cat0)
        print "1: " + random_word(cat1)
