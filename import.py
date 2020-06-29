import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://arbmbhqjarunnk:fdf2eb529c2e475cb412d1a83e57e980a2c3e12c1da58a5c8764c75830c0e80f@ec2-18-214-119-135.compute-1.amazonaws.com:5432/d8384s9us93s4q")
db = scoped_session(sessionmaker(bind = engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book {title} by {author}, {year} with isbn {isbn}")
    db.commit()

if __name__ == "__main__":
    main()