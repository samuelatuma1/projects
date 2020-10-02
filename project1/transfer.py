from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



app = Flask(__name__)

import csv
import os
DATABASE_URI = 'postgres://ttbcugxkaynqlk:1c55b1b6ba13d4b887bc0274e526ef3eb3e7786be5c00c5928f8ff596ec10a66@ec2-46-137-124-19.eu-west-1.compute.amazonaws.com:5432/d8orpnsjlkp3g'


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(DATABASE_URI)
db = scoped_session(sessionmaker(bind=engine))

db.execute('CREATE TABLE users (id SERIAL PRIMARY KEY, usernames VARCHAR NOT NULL, passwords VARCHAR NOT NULL);')