#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word

import requests
import json
import random
import database as db

f = open("./.secrets.txt", 'rU')
keys = json.loads(f.read())
f.close()

GIPHY_KEY = keys['giphy']

GIPHY_URL = "http://api.giphy.com/v1/"
DATAMUSE_URL = "http://api.datamuse.com/words?"

GIF_TYPE = 'fixed_width_small'

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
def find_gifs(query, limit=4, offset=0):
    url = GIPHY_URL + 'gifs/search?'
    print query
    params = {
            'api_key': GIPHY_KEY,
            'q': query,
            'rating': 'pg',
            'limit': limit,
            'offset': offset,
           }
    res = requests.get(url, params=params)
    gifs = res.json()
    return gifs['data']

def gifs_for_word(category, word, use_category=True):
    db_word = db.get_word(category, word)
    if db_word:
        gifs = db_word[2:]
    else:
        query = word
        if use_category:
            query += " " + category
        gifs = find_gifs(query)
        gif_list = list()
        for gif in gifs:
            gif_list.append(gif['images'][GIF_TYPE]['url'])
        lst = [category, word]
        lst.extend(gif_list)
        if db.save_word(category, word, gif_list):
            print "Saved [" + word  + "] in category: " + category
        else:
            print "Error saving [" +  word  + "] in category: " + category
        gifs = lst[2:]
    return gifs

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
    db.setup()
    gifs_for_word('foodstuff', 'coffee')
