import requests
import datetime
import os
DATABASE_URI = 'postgres+psycopg2://postgres:2888627777s@localhost:5432/postgres'

from flask import Flask, session,  render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify



app = Flask(__name__)
app.secret_key="secret"


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(DATABASE_URI)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def signin():
    name = db.execute("SELECT * FROM users WHERE usernames=:username AND passwords=:password", {"username": 'AtumaSamuel' , "password": 'password'}).fetchone()
    session["user_id"] = name
    return session["user_id"].usernames

@app.route("/new")
def just():
    return session["user_id"].passwords

@app.route("/news")
def justy():
    user_id = session.get("user_id")
    return render_template('error.html', message = user_id.passwords)

