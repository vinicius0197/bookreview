# Book Review Project

This simple web app was developed for the CS50 Web Programming with Python and Javascript course. This is a simple web application for book reviewing.

## Objectives

- Get used with Flask web development
- Practice with SQL and PostgreSQL
- Get started with API requests and development

## Getting Started

To use this project, first git clone this repository and install the requirements by using:

```
pip3 install -r requirements.txt
```

This will install Flask and other dependencies.

You need to tell Flask which file will run the application. If you are using Linux:

```
export FLASK_APP=application.py
```

I've used a PostgreSQL database hosted at Heroku for this project, but you can host the database on your own computer if you want. Just remember to create a .env file containing the link to this database and, if you want to use integration with Goodreads API, also an API key, as the following:

```
DATABASE_URL=your_database_url
GOODREADS_KEY=your_goodreads_key
```

I've created a simple Python script called *import.py* for uploading the .csv data to the database. This script performance is not optimal, so it may take some time uploading all rows.

After the database is set, you can start the web app by running:

```
flask run
```

The front-end for this web application is very simple and not user friendly at all. My main goal with this project was just learning more about the back-end and getting used with databases and Flask web development.

I may come back in the future and upload some new designs, and also add new features.