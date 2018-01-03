#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word

import requests
import json
import random

f = open("./.secrets.txt", 'rU')
keys = json.loads(f.read())
f.close()

GIPHY_KEY = keys['giphy']

GIPHY_URL = "http://api.giphy.com/v1/"
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

def valid_word(word, allow_proper=False):
    '''
    valid_word returns whether a word is allowed based on the
    following conditions:
        * between 3-10 letters,
        * no spaces,
        * score at least 100,
        * a noun that is not proper.

    If allow_proper is true, then proper nouns are allowed.
    '''
    if ' ' in word['word']:
        return False

    l = len(word['word'])
    if l < 3 or l > 10:
        return False

    if word['score'] < 100:
        return False

    if 'n' not in word['tags']:
        return False

    if not allow_proper and 'prop' in word['tags']:
        return False

    return True

# Return a random hyponym given the list of filtered words
def random_word(words):
    return random.choice(words)['word']

# Find 4 gifs given the query and category
# Optional usage of category
def find_gifs(query, category, use_category=False):
    url = GIPHY_URL + 'gifs/search?'
    if use_category:
        query += ' ' + category
    print query
    params = {
            'api_key': GIPHY_KEY,
            'q': query,
            'rating': 'pg',
            'limit': 4,
           }
    res = requests.get(url, params=params)
    gifs = res.json()
    return gifs['data']

if __name__ == "__main__":
    print(CATEGORIES)
    cat0 = filter(valid_word, find_hyponyms(CATEGORIES[0]))
    cat1 = filter(valid_word, find_hyponyms(CATEGORIES[1]))
    print len(cat0)
    print len(cat1)
    # for w in cat0:
    #     print w['word']
    for i in range(5):
        print "0: " + random_word(cat0)
        print "1: " + random_word(cat1)

    # print find_gifs('donut')
