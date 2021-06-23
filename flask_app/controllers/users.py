from flask.globals import session
from flask_app.config.mysqlconnection import log_this
from flask import Flask, render_template, request, redirect
from flask import flash

from flask_app import app  
from flask_app.models import user
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():   # call the get all classmethod to get all users
    print("in index route")
    return render_template("index.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    if not User.validate_login(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form["password"])

    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }

    # We pass the data dictionary into the save method from the Friend class.
    log_this("create user - app route", data, "", "")
    
    User.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/')

@app.route("/success")
def go_to_success_page():
    if not "user_id" in session:
        flash("Please login to continue using this site!")
        return redirect("/")
    data = {
        "id" : session["user_id"]
    }
    user = User.get_user_by_id(data)
    return render_template("success.html", user = user)

@app.route("/login_user", methods=["POST"])
def login_user():
    data = {
        'email' : request.form["login_email"],
        'password' : request.form["login_password"]
    }
    user_in_db = User.get_user_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password. Please check your credentials and try again.")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form["login_password"]):
        #if password match is false
        flash("Invalid Email/Password.  Please check your credentials and try again.")
        return redirect("/")

    # here, everything checks out, set session id for user    
    session['user_id'] = user_in_db.id

    return redirect("/success")


@app.route("/logout")
def logout():
    session.clear()
    flash("You were successfully logged out!  Have a great day!")
    return redirect("/")