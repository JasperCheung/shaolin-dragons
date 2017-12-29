#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word

from flask import Flask, render_template, request, redirect, flash, Markup, url_for
import requests, os
# from util import

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

if __name__ == "__main__":
    app.debug = True
    app.run()
