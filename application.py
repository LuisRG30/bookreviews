import os

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup", methods = ["POST"])
def signup():
    username = request.form.get("uname")
    password = request.form.get("password")

    #Try to get an existing user in database
    possible_user = User.query.filter_by(username = username).first()
    if possible_user:
        return render_template("error.html", message="Username not available.")
    newuser = User(username, password)
    newuser.add_user()
    return render_template("sucess.html", message="User account created successfully.")
