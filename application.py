import os

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
    password = request.form.get("psw")

    #Try to get an existing user in database
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0:
        return render_template("error.html", message="Username \"" + username + "\" is not available.")

    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
    {"username": username, "password": password})
    db.commit()
    return render_template("success.html", message="User account created successfully.")

@app.route("/books", methods = ["GET", "POST"])
def books():
    if request.method == "POST":
        #Get form data
        username = request.form.get("uname")
        password = request.form.get("psw")

        if username is None or password is None:
            return render_template("error.html", message="User not logged in.")

        #Query for user in database
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if user is None:
            return render_template("error.html", message="There is no acount associated with username \"" + username + "\".")
        if password != user.password:
            return render_template("error.html", message="Incorrect username or password.")
        
        #Save user's session
        if session.get("id") is None:
            session["id"] = user.id

    if request.method == "GET":
        if session.get("id") is None:
            return render_template("error.html", message="User not logged in.")

    #Query for books
    books = db.execute("SELECT * FROM books").fetchall()

    return render_template("books.html", books=books)
    
@app.route("/books/<int:book_id>")
def book(book_id):
    #Check if requested book exists
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    if book is None:
        return render_template("error.html", message="Book not found.")
    #Render template with book details
    return render_template("book.html", book=book)

@app.route("/signout", methods = ["POST"])
def signout():
    session.clear()
    return render_template("success.html", message="Logged out successfully.")