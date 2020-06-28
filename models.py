from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    def add_user(self):
        u = User(username = self.username, password = self.password)
        db.session.add(u)
        db.session.commit()

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)

    def add_review(self, score, review):
        r = Review(score = score, review = review, book_id = self.id)
        db.session.add(r)
        db.session.commit()

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Integer, nullable = False)
    review = db.Column(db.String, nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)
