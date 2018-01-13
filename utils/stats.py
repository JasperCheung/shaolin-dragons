#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word


''' List of methods
words_solved() - returns int
num_users() - returns int
num_words_flagged() - returns int
num_gifs_flagged() - returns int
next_high_score(user) - returns (String, int)
                                  (other_user, next_higher_score)
'''

import sqlite3
import database
global db

#WORDS SOLVED IN ALL OF HISTORY
def words_solved():
    global db
    try:
        c=database.open_db()
        command = "SELECT pts FROM accounts"
        c.execute(command)
        data = c.fetchall()
        database.close_db()
    except:
        print "Error: could not get words solved"
        return 0
    total = 0
    for entry in data:
        total += entry[0]/100
    return total

#NUMBER OF USERS IN ALL OF HISTORY
def num_users():
    global db
    try:
        c=database.open_db()
        command = "SELECT * FROM accounts"
        c.execute(command)
        data = c.fetchall()
        database.close_db()
    except:
        print "Error: could not get number of users"
        return 0
    count = 0
    for entry in data:
        count += 1
    return count

#NUMBER OF WORDS FLAGGED
def num_words_flagged():
    global db
    try:
        c=database.open_db()
        command = "SELECT * FROM flaggedword"
        c.execute(command)
        data = c.fetchall()
        database.close_db()
    except:
        print "Error: could not get number of words flagged"
        return 0
    count = 0
    for entry in data:
        count += 1
    return count

#NUMBER OF GIFS FLAGGED
def num_gifs_flagged():
    global db
    try:
        c=database.open_db()
        command = "SELECT * FROM flaggedgif"
        c.execute(command)
        data = c.fetchall()
        database.close_db()
    except:
        print "Error: could not get number of gifs flagged"
        return 0
    count = 0
    for entry in data:
        count += 1
    return count

#GET USER WITH NEXT HIGHER SCORE
def next_high_score(user):
    global db
    try:
        score = database.get_score(user)
        c=database.open_db()
        command = "SELECT user,pts FROM accounts WHERE pts>? ORDER BY pts ASC"
        c.execute(command, (score,))
        data = c.fetchone()
        database.close_db()
    except:
        print "Error: could the next higher score"
        return None
    return data

print words_solved()
#print num_users()
#print num_words_flagged()
#print num_gifs_flagged()
#print next_high_score("jack")
