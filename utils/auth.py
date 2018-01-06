#Shaolin Dragons
#Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
#SoftDev pd7
#P02 - 4Gifs1Word

from flask import redirect, url_for, request, session, flash, Markup
import database

# Signs up user and routes to categories
def signup():
    username = request.form.get("username")
    pass0 = request.form.get("password")
    pass1 = request.form.get("confirm_password")
    isValid = database.create_acc(username, pass0, pass1)
    # Returns (boolean, boolean) where
    # isValid[0] represents if the username is valid
    # isValid[1] represents if the passwords match
    if not isValid[0]:
        flash(Markup("Username <b>" + username.upper() + "</b> already exists. Please choose another one."),"warning")
        return redirect("signup")
    if not isValid[1]:
        flash("Passwords do not match. Please try again.","warning")
        return redirect("signup")
    else:
        session["username"] = username
        flash(Markup("Welcome to 4 GIFS 1 WORD, <b>" + username.upper() + "</b>!"),"warning")
        return redirect("")


# Logs in user and routes to categories
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if database.auth(username,password): # If
        session["username"] = username # Adds username to session
        return redirect("")
    else:
        flash("Invalid username or password. Please try again.","warning")
        return redirect("login")
