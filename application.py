import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv, find_dotenv
from passlib.hash import pbkdf2_sha256

# Loads environment variables from .env file
load_dotenv(find_dotenv())

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
    return render_template("layout.html")

@app.route("/registration")
def registration():
	"""

	Renders registration form

	"""
	return render_template('registration.html')

@app.route("/registrate_user", methods=['POST'])
def registrate_user():
	"""
	
	Registrate a user into database using form data
	
	"""

	# Get form information
	username = request.form.get("username")
	pwd = request.form.get("password")

	# Encrypt password using python passlib library
	hash = pbkdf2_sha256.encrypt(pwd, rounds=200000, salt_size=16)

	db.execute("INSERT INTO users (username, password) VALUES (:username, :pwd)", {"username": username, "pwd": hash})
	db.commit()

	return render_template('registration.html')
