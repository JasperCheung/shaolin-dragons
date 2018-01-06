#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word

from flask import Flask, render_template, request, redirect, flash, Markup, url_for, session
import requests, os
from utils import database as db
from utils import api
from utils import auth

app = Flask(__name__)
app.secret_key = os.urandom(128)

# Landing page; displays the home page
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", username = username(), logged_in = logged_in(), score = score())

# Displays the sign-up page and executes sign up procedures
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("username"):
        return redirect("")
    elif request.form.get("signup"):
        return auth.signup()
    else:
        return render_template("signup.html", score = score())

# Displays the log-in page and executes log in procedures
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect("")
    elif request.form.get("login"):
        return auth.login()
    return render_template("login.html", score = score())

# Logs out user (removes from session) and routes to home
@app.route("/logout", methods=["GET", "POST"])
def logout():
    if logged_in():
        session.pop("username")
        flash("Logged out.","warning")
    return redirect("/")


@app.route("/categories")
def categories():
    count = 0
    text = ""
    for cat in api.CATEGORIES:
        if count == 0:
            text += "<div class='row home-btns'>"
        text += "<div class='col-sm-4'>"
        text += "<a href='/game?category=" + cat + "'>"
        text += "<div class='card card-animate'>"
        text += "<h1>" + cat + "</h1>"
        text += "</div></a></div>"
        if count == 2:
            text += "</div>"
            count = 0
        else:
            count = count + 1
    if count != 0:
        # Uncommenting this will uncenter the categories; just leave this
        # for x in range(count, 3):
        #    text += "<div class='col-sm-4'></div>"
        text += "</div>"
    return render_template("categories.html", categories = Markup(text), username = username(), logged_in = logged_in(), score = score())


@app.route("/game")
def game():
    args = request.args
    if "category" not in args:
        flash("You must select a category to play the game", "warning")
        return redirect(url_for("categories"))
    print "finding word"
    category = args["category"]
    hyponyms = filter(api.valid_word, api.find_hyponyms(category))
    word = api.random_word(hyponyms)
    # Maybe make it so use category for specific categories
    gifs = api.gifs_for_word(category, word)
    return render_template("game.html", gifs = gifs, word = word, category = category, username = username(), logged_in = logged_in(), score = score())

@app.route("/gif_flag")
def gif_flag():
    return "gif flagged"

@app.route("/rankings")
def leaderboard():
    return render_template("rankings.html", username = username(), logged_in = logged_in(), score = score())

@app.route("/appfun")
def appstats():
    return render_template("appfun.html", username = username(), logged_in = logged_in(), score = score())

@app.route("/error")
def error():
    return render_template("error.html", username = username(), logged_in = logged_in(), score = score())

# Checks if logged in
def logged_in():
    return session.get("username")

# Returns username
def username():
    if logged_in():
        return session["username"].upper()
    else:
        return "GUEST"

# Returns score of the logged in person/guest
def score():
    if logged_in():
        return db.get_score(username())
    elif session.get("score"):
        return session["score"]
    else:
        session["score"] = "0"
        return "0"

if __name__ == "__main__":
    app.debug = True
    db.setup()
    app.run()
