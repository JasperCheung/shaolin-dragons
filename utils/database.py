#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word


''' List of methods
setup() - sets up db

create_acc(user,pwd1,pwd2) - sees if input is valid, adds acc to db
    returns (T/F, T/F) -- (is username valid, is password valid)

auth(user,pwd) - checks if user and pwd match
    returns T/F

update_pts(user,pts) - updates points of user
    returns T/F

get_score(user) - gets score of one user
    returns score or None

get_scores() - gets scores of all users
    returns tuple of scores

add_history(user,cat,word) - adds history
    returns T/F

user_history(user) - procures user's history
    returns collection of tuples with format (category,word) or None

save_word(cat,word,giflst) - add word to database
    returns T/F

get_word(cat,word) - gets gif urls from db if there
    returns (cat,word,g1-g4) or None

update_word(user,cat,giflst) - updates gif urls
    returns T/F

is_gif_flagged(cat,word,url)
    returns T/F

flag_gif(cat,word,url) - flags a gif as problematic
    returns T/F

is_word_flagged(cat,word)
    returns T/F

flag_word(cat,word) - flags a word as problematic
    retuns T/F

gif_offset(cat,word) - finds the number of gifs flagged for this word
    returns int
'''

global db
import sqlite3
import hashlib
from time import gmtime, strftime

#open database
def open_db():
    global db
    f = "data/playgame.db"
    db = sqlite3.connect(f, check_same_thread = False)
    return db.cursor()

#close database
def close_db():
    global db
    db.commit()
    db.close()
    return

#SETUP - TO BE RUN EACH TIME
#------------------------------------
def setup():
    c= open_db()
    stmt= "CREATE TABLE IF NOT EXISTS accounts(user TEXT PRIMARY KEY, pass TEXT, pts INTEGER)"
    c.execute(stmt)
    stmt= "CREATE TABLE IF NOT EXISTS flaggedgif(category TEXT, word TEXT, url TEXT, PRIMARY KEY (category, word, url))"
    c.execute(stmt)
    stmt = "CREATE TABLE IF NOT EXISTS flaggedword(category TEXT, word TEXT, PRIMARY KEY (category, word))"
    c.execute(stmt)
    stmt = "CREATE TABLE IF NOT EXISTS history(user TEXT, category TEXT, word TEXT, PRIMARY KEY (user, category, word))"
    c.execute(stmt)
    stmt = "CREATE TABLE IF NOT EXISTS saved(category TEXT, word TEXT, g1 TEXT, g2 TEXT, g3 TEXT, g4 TEXT, PRIMARY KEY (category, word))"
    c.execute(stmt)
    close_db()
    return
#=====================================


#CREATE AN ACCOUNT
#-------------------------------------
def create_acc(user, pwd1, pwd2):
    global db
    try:
        user=user.strip().lower()
        c = open_db()
        #hashing pwd
        obj = hashlib.sha224(pwd1)
        hash_pwd = obj.hexdigest()

        command = "INSERT INTO accounts VALUES(?,?,0)"
        c.execute(command, (user,hash_pwd)) #try to see if user exists
        #if pwds don't match
        if pwd1 != pwd2:
            db.close() #don't commit and close
            return (True, False)
        else:
            close_db() #commit and close
            return (True, True)

    except: #if user exists, code will jump here
        print "Error: account cannot be created"
        return (False, False)

#=======================================


#AUTHENTICATE USER
#---------------------------------------
#returns true or false
#previously (has passwords?, correct password?)
def auth(user, pwd):
    global db
    try:
        user=user.strip().lower()
        c = open_db()
        command = "SELECT pass FROM accounts WHERE user=?"
        c.execute(command, (user,))
        pwds = c.fetchall()
        close_db()
    except:
        print "Error: authenticate call not made"
        return False #(False, False)
    if len(pwds) == 0:
        return False #(False, False)
    #hashing pwd
    obj = hashlib.sha224(pwd)
    hash_pwd = obj.hexdigest()
    if pwds[0][0] == hash_pwd:
        return True #(True, True)
    else:
        return False #(False, True)
#========================================


#UPDATE POINTS
#----------------------------------------
def update_pts(user, pts):
    global db
    try:
        c = open_db()
        command = "UPDATE accounts SET pts =? WHERE user=?"
        c.execute(command,(pts,user))
        close_db()
    except:
        print "Error: points not updated"
        return False
    return True
#========================================


#GET ONE USER'S POINTS
#----------------------------------------
def get_score(user):
    global db
    try:
        c = open_db()
        command = "SELECT pts FROM accounts WHERE user=?"
        c.execute(command, (user,))
        score = c.fetchone()[0]
        close_db()
    except:
        print "Error: could not get score"
        return None
    return score
#========================================


#GET ALL SCORES
#----------------------------------------
def get_scores():
    global db
    try:
        c = open_db()
        command = "SELECT user,pts FROM accounts ORDER BY pts DESC"
        c.execute(command)
        data = c.fetchall()
        close_db()
    except:
        print "Error: could not get scores"
        return (None)
    count = 1
    scores = {}
    for entry in data:
        scores[count] = entry
        count += 1
    return scores
#========================================


#ADD TO HISTORY
#----------------------------------------
def add_history(user, cat, word):
    global db
    try:
        c= open_db()
        command= "INSERT INTO history VALUES (?,?,?)"
        c.execute(command, (user,cat,word))
        close_db()
    except:
        print "Error: could not add history"
        return False
    return True
#========================================


#GET A USER'S HISTORY
#----------------------------------------
def user_history(user):
    global db
    try:
        c= open_db()
        command= "SELECT category,word FROM history WHERE user=?"
        c.execute(command, (user,))
        data=c.fetchall()
        close_db()
    except:
        print "Error: could not get user history"
        return None
    return data
#========================================


#ADD TO SAVED WORDS
#----------------------------------------
def save_word(cat,word,giflst):
    global db
    try:
        c= open_db()
        lst = [cat,word]
        lst.extend(giflst)
        lst = fill_list(lst,6)
        print lst
        command = "INSERT INTO saved VALUES (?,?,?,?,?,?)"
        c.execute(command, tuple(lst))
        close_db()
    except:
        print "Error: could not save word"
        return False
    return True

def fill_list(lst,n):
    while len(lst) < n:
        lst.append(None)
    return lst
#========================================


#GET WORD IF EXISTS IN TABLE
#----------------------------------------
def get_word(cat,word):
    global db
    try:
        c= open_db()
        command = "SELECT * FROM saved WHERE category=? AND word=?"
        c.execute(command, (cat,word))
        data= c.fetchone()
       # print data
        close_db()
    except:
        print "Error: could not retrieve word"
        return None
    return data
#========================================


#UPDATE SAVED GIFS URL
#----------------------------------------
def update_word(cat,word,giflst):
    global db
    try:
        c= open_db()
        lst = fill_list(giflst,4)
        print lst
        lst.append(cat)
        lst.append(word)
        command = "UPDATE saved SET g1=?,g2=?,g3=?,g4=? WHERE category=? AND word=?"
        c.execute(command, tuple(lst))
        close_db()
    except:
        print "Error: could not update word"
        return False
    return True
#========================================


#CHECK IF GIF IS FLAGGED
#----------------------------------------
def is_gif_flagged(word, cat, url):
    global db
    try:
        c= open_db()
        command = "INSERT INTO flaggedgif VALUES (?,?,?)"
        c.execute(command, (word,cat,url))
        db.close()
    except:
        return True
    return False
#========================================


#FLAG A GIF
#----------------------------------------
def flag_gif(cat, word, url):
    global db
    try:
        c= open_db()
        command = "INSERT INTO flaggedgif VALUES (?,?,?)"
        c.execute(command, (cat, word ,url))
        close_db()
    except:
        print "Error: could not flag gif"
        return False
    return True
#========================================


#CHECK IF WORD IS FLAGGED
#----------------------------------------
def is_word_flagged(cat, word):
    global db
    try:
        c=open_db()
        command = "INSERT INTO flaggedword VALUES(?,?)"
        c.execute(command, (cat,word))
        db.close()
    except:
        return True
    return False
#========================================


#FLAG A WORD
#----------------------------------------
def flag_word(cat, word):
    global db
    try:
        c=open_db()
        command = "INSERT INTO flaggedword VALUES(?,?)"
        c.execute(command, (cat,word))
        close_db()
    except:
        print "Error: could not flag word"
        return False
    return True
#========================================

#FIND GIF OFFSET
#----------------------------------------
def gif_offset(cat, word):
    global db
    try:
        c=open_db()
        command="SELECT * FROM flaggedgif WHERE category=? AND word=?"
        c.execute(command, (cat,word))
        data=c.fetchall()
    except:
        print "Error: could not get gif offset"
        return 0
    count = 0
    for entry in data:
        count += 1
    return count
#========================================
#-TEST-TEST-TEST-TEST-TEST-TEST-
# if __name__ == "__main__":
setup()
#print create_acc("jon", "snow", "hail") #t,f
#print create_acc("jack", "snow", "snow") #t,t
#print create_acc("jon", "snow", "hail") #f,f
#print create_acc("jon", "snow", "snow") #f,f

#print auth("jon","snow") #both correct t
#print auth("jack","snow") #user wrong f
#print auth("jon","slew") #pwd wrong f

#print update_pts("jon", 60)
#print update_pts("jack", 20) #will not say anything if username wrong, but is still not inputted

#create_acc("bilbo","baggins")
#update_pts("bilbo", 120)
#print get_score("bilbo") #120
#print get_scores()#returns [(u'bilbo', 120),(u'jon', 60)]

#print add_history("jon", "emotions", "happy")
#print add_history("jon", "phrase", "yolo")
#print user_history("jon")

#print save_word("c1","w1",["g1","g2","g3","g4"])
#print save_word("c1","w2",["g1","g2","g3"])
#print save_word("c2","w1",["g1","g2"])
#print save_word("c1","w1",["g1","g2","g3","g4"]) #error

#print get_word('c1','w2') #(u'c1', u'w2', u'g1', u'g2', u'g3', None)
#print get_word('c3','w1') # None

#print update_word('c1','w2', ['g1'])

#print is_gif_flagged('c1','w2','ggg') #f
#print flag_gif('c1','w2','ggg')#t
#print is_gif_flagged('c1','w2','ggg')#t

#print is_word_flagged('c3','w4') #f
#print flag_word('c3','w4') #t
#print is_word_flagged('c3','w4') #t

#print flag_gif('c1','w2','gggg')#t
#print flag_gif('c1','w2','ggg')#t
#print flag_gif('c1','w2','gg')#t
#print flag_gif('c1','w2','g')#t
#print gif_offset('c1','w2')#should return 4
