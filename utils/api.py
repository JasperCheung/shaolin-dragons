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

GIF_TYPE = 'fixed_width'

CATEGORY_LOC = './static/categories/'

f = open(CATEGORY_LOC + "categories.json", 'rU')
CATEGORIES = json.loads(f.read())
f.close()

# ADD FINDING A CATEGORY IN THE LOCAL DIRECTORY BEFORE USING Datamuse

# This has to do with using the .txt files

# Given a category, return a list of the words that Datamuse returns
def find_hyponyms(category):
    # If the category is just a list of words 
    is_file = False
    try:
        path = CATEGORY_LOC + category + ".txt"
        with open(path) as f:
            words = f.readlines()
        words = [word.strip() for word in words]
        print path
        is_file = True
    except FileNotFoundError:
        url = DATAMUSE_URL + 'md=p&rel_gen={}'.format(category)
        res = requests.get(url)
        words = res.json()
    return words, is_file

def valid_word(word, category="", allow_proper=False):
    '''
    valid_word returns whether a word is allowed based on the
    following conditions:
        * between 3-10 letters,
        * no spaces,
        * score at least 100,
        * a noun that is not proper.
        * has been flagged

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

    if db.is_word_flagged(category,word['word']):
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
            'rating': 'g',
            'limit': limit,
            'offset': offset,
           }
    res = requests.get(url, params=params)
    gifs = res.json()
    return gifs['data']

def gifs_for_word(category, word, use_category=True):
    print "GIFs for: " +  word + "--" + category
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

# Returns False if fails
def flag_gif(category, word, gif_url, use_category=True):
    db_word = db.get_word(category, word)
    if db_word is None:
        # DO SOMETHING IF IT FAILS
        print "Could not retrieve word, could not flag"
        return False
    query = word
    if use_category:
        query += " " + category
    flagged = db.flag_gif(category, word, gif_url)
    if not flagged:
        print "Failed to flag."
        return False
    offset = db.gif_offset(category, word) + 4
    new = find_gifs(query, limit=1, offset=offset)
    new = new[0]['images'][GIF_TYPE]['url']
    new_gifs = list(db_word)
    new_gifs.remove(gif_url)
    new_gifs.append(new)
    db.update_word(new_gifs[0], new_gifs[1], new_gifs[2:])
    print "Flagged gif: [" + gif_url + "]"
    print "Updated word: [" + word + "]"
    return True

# Returns False if fails
def flag_word(category, word, use_category=True):    
    query = word
    if use_category:
        query += " " + category
    if not db.flag_word(category, word):
        print "Failed to flag word."
        return False
    print "Flagged word: [" + query + "]"
    return True

if __name__ == "__main__":
    print(CATEGORIES)
    cat0 = filter(valid_word, find_hyponyms(CATEGORIES['Food']))
    cat1 = filter(valid_word, find_hyponyms(CATEGORIES['Drinks']))
    print len(cat0)
    print len(cat1)
    # for w in cat0:
    #     print w['word']
    for i in range(5):
        print "0: " + random_word(cat0)
        print "1: " + random_word(cat1)

    # print find_gifs('donut')
    db.setup()
    print gifs_for_word('foodstuff', 'coffee')
    print flag_gif('foodstuff', 'coffee', 'https://media1.giphy.com/media/Z6vszQ8Mweukw/200w.gif')
    print gifs_for_word('foodstuff', 'coffee')
