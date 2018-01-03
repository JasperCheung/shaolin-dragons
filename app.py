#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word

from flask import Flask, render_template, request, redirect, flash, Markup, url_for
import requests, os
from utils import database as db
from utils import api

app = Flask(__name__)
app.secret_key = os.urandom(128)

# Landing page; displays the home page
@app.route("/")
def home():
    return render_template("home.html")
# Displays the sign-up page
# If credentials are valid, routes to game page
@app.route("/sign_up")
def sign_up():
    return render_template("signup.html") # Page does not exist yet

# Displays the log-in page
# If credentials are valid, routes to game page
@app.route("/log_in")
def log_in():
    return render_template("login.html") # Page does not exist yet

@app.route("/categories")
def categories():
    return render_template("categories.html", categories=api.CATEGORIES)

@app.route("/game")
def game():
    args = request.args
    if 'category' not in args:
        flash("You must select a category to play the game", 'warning')
        return redirect(url_for('categories'))
    print "finding word"
    category = args['category']
    hyponyms = filter(api.valid_word, api.find_hyponyms(category))
    word = api.random_word(hyponyms)
    # Maybe make it so use category for specific categories
    gifs = api.find_gifs(word, category, use_category=True)
    return render_template('game.html', gifs=gifs)

if __name__ == "__main__":
    app.debug = True
    db.setup()
    app.run()
