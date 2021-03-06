#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word

from flask import Flask, render_template, request, redirect, flash, Markup, url_for, session
import requests, os, json
import random
from utils import database as db
from utils import api
from utils import auth
from utils import game_tools
from utils import stats

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
        return render_template("signup.html", username = username(), logged_in = logged_in(), score = score())

# Displays the log-in page and executes log in procedures
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect("")
    elif request.form.get("login"):
        return auth.login()
    return render_template("login.html", username = username(), logged_in = logged_in(), score = score())

# Logs out user (removes from session) and routes to home
@app.route("/logout", methods=["GET", "POST"])
def logout():
    if logged_in():
        session.pop("username")
        flash("Logged out.","warning")
    return redirect("/")

# Displays categories page
@app.route("/categories")
def categories():
    return render_template("categories.html", categories = api.CATEGORIES, username = username(), logged_in = logged_in(), score = score())

# Displays game page
@app.route("/game")
def game():
    args = request.args
    if "category" not in args:
        flash("Please select a category to play the game.", "warning")
        return redirect("categories")

    print "FINDING WORD..."
    category = args["category"]
    words, is_file = api.find_hyponyms(category)

    if words is None:
        return redirect(url_for("error"))

    hyponyms = [word for word in words if api.valid_word(word, username(), category=category, is_file=is_file)]
    if len(hyponyms) == 0:
        flash("No words left in category!", "warning")
        return redirect(url_for("categories"))
    word = api.random_word(hyponyms, is_file=is_file)

    session["word"] = word

    gifs = api.gifs_for_word(category, word)
    if gifs is None:
        return redirect(url_for('error'))

    bank_length = 12
    letters = game_tools.random_letter_list(word, bank_length)
    session["bank_length"] = bank_length

    return render_template("game.html", gifs = gifs, word = word, \
            category = category, letters = letters, username = username(), \
            logged_in = logged_in(), score = score())

# Return current game's word and
@app.route("/play")
def play():
    response = { "word" : session["word"], "bank_length" : session["bank_length"] }
    return json.dumps(response)

@app.route("/win")
def win():
    data = request.args
    word = data.get("word").upper()
    category = data.get("category")
    if logged_in():
        db.update_pts(username(),int(score()) + 100)
        db.add_history(username(), category, word)
    else:
        session["score"] = str(int(score()) + 100)
    flash(Markup("You scored 100 points for guessing <b>" + word + "</b>! Solve another word."), "success")
    return redirect(url_for("game", category = category))

@app.route("/gif_flag")
def gif_flag():
    args = request.args
    if 'category' not in args or 'word' not in args or 'url' not in args:
        flash("Not enough information received to flag gif!", "danger")
        return redirect(url_for("categories"))
    category = args['category']
    word = args['word']
    url = args['url']
    flagged = api.flag_gif(category, word, url)
    if flagged:
        flash("GIF successfully flagged. Solve a new word.", "warning")
    else:
        flash("Failed to flag GIF.", "danger")
    return redirect(url_for("game", category = request.args["category"]))

@app.route("/word_flag", methods=['GET', 'POST'])
def word_flag():
    args = request.args
    if 'category' not in args or 'word' not in args:
        flash("Not enough information received to flag word.", "danger")
        return redirect(url_for("game", category = request.args["category"]))
    category = args['category']
    word = args['word']
    flagged = api.flag_word(category, word)
    if flagged:
        flash("Word successfully flagged. Solve a new word.", "warning")
    else:
        flash("Failed to flag word.", "warning")
    return redirect(url_for("game", category = args["category"]))

@app.route("/rankings")
def rankings():
    return render_template("rankings.html", rankings = db.get_scores(), username = username(), logged_in = logged_in(), score = score())

@app.route("/appfun")
def appfun():
    stat = [
        ["people playing worldwide", stats.num_users()],
        ["words solved by you", str(int(score())/100)],
        ["words solved by everyone", stats.words_solved()],
        ["words flagged by everyone", stats.num_words_flagged()],
        ["gifs flagged by everyone", stats.num_gifs_flagged()]
    ]
    return render_template("appfun.html", username = username(), logged_in = logged_in(), score = score(), stat = stat)

@app.route("/error")
def error():
    return render_template("error.html", username = username(), logged_in = logged_in(), score = score())

# Checks if logged in
def logged_in():
    return "username" in session

# Returns username
def username():
    if logged_in():
        return session["username"].upper()
    else:
        return "GUEST"

# Returns score of the logged in person/guest
def score():
    if logged_in():
        return db.get_score(username().lower())
    elif "score" in session:
        return session["score"]
    else:
        session["score"] = "0"
        return "0"

if __name__ == "__main__":
    app.debug = True
    db.setup()
    app.run()
