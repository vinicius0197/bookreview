"""
	Imports book data from CSV file for usage in web application

"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv, find_dotenv
import csv

load_dotenv(find_dotenv())

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


with open('books.csv', newline='') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		print(row)
		db.execute("INSERT INTO books (isbn, author, title, year) VALUES (:isbn, :author, :title, :year)", \
			{"isbn": row[0], "author": row[1], "title": row[2], "year": row[3]})
		db.commit()
