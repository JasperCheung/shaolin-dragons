#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word


''' List of methods
create_acc(user,pwd) - adds acc to db
    returns T/F

auth(user,pwd) - checks if user and pwd match
    returns (T/F,T/F): (if there is a user, if the pwd matches)

update_pts(user,pts) - updates points of user
    returns T/F

get_score(user) - gets score of one user
    returns score

get_scores() - gets scores of all users
    returns tuple of scores 

add_history(user,cat,word) - adds history
    returns T/F

user_history(user) - procures user's history
    returns collection of tuples with format (category,word) or None

save_word(cat,word,giflst) - add word to database
    returns T/F

get_word(cat,word) - gets gif urls from db if there
    returns [T/F, (cat,word,g1-g4)]

update_word(user,cat,giflst) - updates gif urls
    returns T/F
'''

global db
import sqlite3
import hashlib
from time import gmtime, strftime

#open database
def dbopen():
    global db
    f = "something.db"
    db = sqlite3.connect(f, check_same_thread = False)
    return db.cursor()

#close database
def dbclose():
    global db
    db.commit()
    db.close()
    return

#SETUP - TO BE RUN EACH TIME
#------------------------------------
c= dbopen()
stmt= "CREATE TABLE IF NOT EXISTS accounts(user TEXT PRIMARY KEY, pass TEXT, pts INTEGER)"
c.execute(stmt)
stmt= "CREATE TABLE IF NOT EXISTS flaggedgif(category TEXT, word TEXT, url TEXT, PRIMARY KEY (category, word))"
c.execute(stmt)
stmt = "CREATE TABLE IF NOT EXISTS flaggedword(category TEXT, word TEXT, PRIMARY KEY (category, word))"
c.execute(stmt)
stmt = "CREATE TABLE IF NOT EXISTS history(user TEXT, category TEXT, word TEXT, PRIMARY KEY (user, category, word))"
c.execute(stmt)
stmt = "CREATE TABLE IF NOT EXISTS saved(category TEXT, word TEXT, g1 TEXT, g2 TEXT, g3 TEXT, g4 TEXT, PRIMARY KEY (category, word))"
c.execute(stmt)
dbclose()
#=====================================


#CREATE AN ACCOUNT
#-------------------------------------
def create_acc(user, pwd):
    global db
    try:
        c = dbopen()
        '''#hashing pwd
        obj = hashlib.sha224(pwd)
        hash_pwd = obj.hexdigest()
        '''
        command = "INSERT INTO accounts VALUES(?,?,0)"
        c.execute(command, (user,pwd))
        dbclose()
    except:
        print "Error: account cannot be created"
        return False
    return True
#=======================================


#AUTHENTICATE USER
#---------------------------------------
#returns (has passwords?, correct password?)
def auth(user, pwd):
    global db
    try:
        c = dbopen()
        command = "SELECT pass FROM accounts WHERE user=?"
        c.execute(command, (user,))
        pwds = c.fetchall()
        dbclose()
    except:
        print "Error: authenticate call not made"
        return (False,False)
    if len(pwds) == 0:
        return (False, False)
    if pwds[0][0] == pwd:
        return (True, True)
    else:
        return (False, True)
#========================================


#UPDATE POINTS
#----------------------------------------
def update_pts(user, pts):
    global db
    try:
        c = dbopen()
        command = "UPDATE accounts SET pts =? WHERE user=?"
        c.execute(command,(pts,user))
        dbclose()
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
        c = dbopen()
        command = "SELECT pts FROM accounts WHERE user=?"
        c.execute(command, (user,))
        score = c.fetchone()[0]
        dbclose()
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
        c = dbopen()
        command = "SELECT user,pts FROM accounts ORDER BY pts DESC"
        c.execute(command)
        scores = c.fetchall()
        dbclose()
    except:
        print "Error: could not get scores"
        return (None)
    return scores
#========================================


#ADD TO HISTORY
#----------------------------------------
def add_history(user, cat, word):
    global db
    try:
        c= dbopen()
        command= "INSERT INTO history VALUES (?,?,?)"
        c.execute(command, (user,cat,word))
        dbclose()
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
        c= dbopen()
        command= "SELECT category,word FROM history WHERE user=?"
        c.execute(command, (user,))
        data=c.fetchall()
        dbclose()
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
        c= dbopen()
        lst = [cat,word]
        lst.extend(giflst)
        lst = fill_list(lst,6)
        print lst
        command = "INSERT INTO saved VALUES (?,?,?,?,?,?)"
        c.execute(command, tuple(lst))
        dbclose()
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
        c= dbopen()
        command = "SELECT * FROM saved WHERE category=? AND word=?"
        c.execute(command, (cat,word))
        data= c.fetchone()
        dbclose()
    except:
        print "Error: could not retrieve word"
        return [False, None]
    if len(data) == 0:
        return [True, None]
    else:
        return [True].append(data)
#========================================


#UPDATE SAVED GIFS URL
#----------------------------------------
def update_word(cat,word,giflst):
    global db
    try:
        c= dbopen()
        lst = fill_list(giflst,4)
        print lst
        lst.append(cat)
        lst.append(word)
        command = "UPDATE saved SET g1=?,g2=?,g3=?,g4=? WHERE category=? AND word=?"
        c.execute(command, tuple(lst))
        dbclose()
    except:
        print "Error: could not update word"
        return False
    return True
#========================================


#CHECK IF GIF IS FLAGGED
#----------------------------------------

#========================================


#FLAG A GIF
#----------------------------------------

#========================================


#CHECK IF WORD IS FLAGGED
#----------------------------------------

#========================================


#FLAG A WORD
#----------------------------------------

#========================================


#-TEST-TEST-TEST-TEST-TEST-TEST-
#print create_acc("jon", "snow") #t
#print create_acc("jon", "snow") #f
#print auth("jon","snow") #both correct t,t
#print auth("jack","snow") #user wrong f,f
#print auth("jon","slew") #pwd wrong f,t

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

print get_word('c1','w2')
