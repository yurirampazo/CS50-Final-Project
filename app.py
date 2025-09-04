from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import bcrypt

from helpers import apology, login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///yulearn.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ORM model for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)

# Create tables if not exist
with app.app_context():
    db.create_all()

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("layout.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", 403)
        if not password:
            return apology("must provide password", 403)

        # Fetch user object using ORM
        user = User.query.filter_by(username=username).first()

        if not user or not bcrypt.verify(password, user.hash):
            return apology("invalid username and/or password", 403)

        session["user_id"] = user.id
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("missing username", 400)
        if not password:
            return apology("missing password", 400)
        if not confirmation:
            return apology("passwords don't match", 400)
        if password != confirmation:
            return apology("passwords don't match", 400)
        if username.strip() == "" or password.strip() == "" or confirmation.strip() == "":
            return apology("blank input not allowed", 400)

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return apology("username taken", 400)

        # Create new user
        hash_pw = bcrypt.hash(password)
        new_user = User(username=username, hash=hash_pw)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        return redirect("/")

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
