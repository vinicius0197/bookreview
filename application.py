import os

from flask import Flask, session, render_template, request, g, redirect, url_for
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

@app.before_request
def before_request():
    if 'logged_in' in session:
    	g.user = session["user"]


@app.route("/")
def index():
    return render_template("index.html")

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


	check_username = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()

	if check_username is None:
		# Encrypt password using python passlib library
		hash = pbkdf2_sha256.encrypt(pwd, rounds=200000, salt_size=16)

		db.execute("INSERT INTO users (username, password) VALUES (:username, :pwd)", {"username": username, "pwd": hash})
		db.commit()

		return render_template('registration.html')
	else:
		return 'Username already taken'

@app.route("/login")
def login():
	"""

	Renders login form

	"""

	return render_template('login.html')

@app.route("/login_user", methods=['POST'])
def login_user():
	"""

	Authenticate user

	"""

	# Get form information
	username = str(request.form.get("username"))
	pwd = str(request.form.get("password"))

	# Queries database to check if username and password exists	
	user_data = db.execute("SELECT password FROM users WHERE username = :username", {"username": username}).fetchone()

	if user_data is None:
		return "This user does not exist"

	if pbkdf2_sha256.verify(pwd, user_data.password):
		session["user"] = username
		session["logged_in"] = True
		return render_template("search.html")

@app.route("/logout")
def logout():
	"""

	Logout user

	"""

	# Remove username from session if it is here
	session.pop('user', None)
	session.pop('logged_in', None)

	return redirect(url_for('index'))

@app.route("/search", methods=['GET', 'POST'])
def search():
	"""
	
	Implements search functionality in the web app

	"""
	if request.method == 'POST':
		search_input = '%' + str(request.form.get("search")) + '%'

		# Queries database for similar results (case insensitive)
		result = db.execute("SELECT * FROM books WHERE isbn LIKE :search \
			OR LOWER(author) LIKE :search \
			OR LOWER(title) LIKE :search \
			OR year LIKE :search", \
			{"search": search_input}).fetchall()

		for row in result:
			print(row)

		return render_template("search.html", result=result)
	else:
		return render_template("search.html")
