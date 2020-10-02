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




#Register
@app.route("/registration")
def registration():
    """Redirects to registration page"""
    return render_template('register.html')


@app.route("/register", methods=["POST"])
def register():
    """Register users includes data in users table"""
    if request.method == "POST":
        username=request.form.get('username')
        password=request.form.get('password')

        #add user to database
        user = db.execute('INSERT INTO users (usernames, passwords) VALUES (:username, :password)', {'username': username, 'password':password})
        db.commit()
        

    return render_template('success.html', username = username)


#Login
@app.route("/login")
def details():
    return render_template('userlogin.html')

@app.route("/loggedin", methods=["POST"])
def login(): 
    username = request.form.get('username')
    password = request.form.get('password')

    user = db.execute(f"SELECT * FROM users WHERE usernames LIKE '%{username}%'", {"username":username}).fetchone()
    if user is None:
        return render_template('error.html', message="No such user.")
     
    secretpass = db.execute("SELECT * FROM users WHERE usernames=:username AND passwords=:password ", {"username":username, "password":password}).fetchone()
    if secretpass:
        use = db.execute("SELECT * FROM users WHERE usernames=:username", {"username":username}).fetchone()
        session["user_id"]=use.id
        
        
        books=db.execute("SELECT * FROM usertable").fetchall()
        
            
        return render_template("loggedin.html", user=session["user_id"])

@app. route("/loggin", methods=["POST"])
def loggedin():
    search = request.form.get('search')
    books=db.execute("SELECT * FROM usertable").fetchall()
    book = False
    for var in books:
        
        if search in var.isbn:
            book = db.execute("SELECT * FROM usertable WHERE isbn=:search", {"search":search}).fetchall()
        elif search in var.title:
            book = db.execute(f"SELECT * FROM usertable WHERE title LIKE '%{search}%'", {"search":search}).fetchall()     
        elif search in var.author:
            book = db.execute("SELECT * FROM usertable WHERE author=:search", {"search":search}).fetchall()         
        elif search in var.year:
            book = db.execute("SELECT * FROM usertable WHERE year=:search", {"search":search}).fetchall()  
    
    if book:
        return render_template('bookpage.html', book=book) 
    elif book== False:
        return "No book"
    

@app.route("/thebook/<int:id>")
def thebook(id):
    # Passing in a session that was created in another function requires you to use the syntax session.get('session_name')
    user_id=session.get('user_id')     
    book = db.execute("SELECT * FROM usertable WHERE id=:id", {"id":id}).fetchone()
    review = db.execute("SELECT * FROM bookreviews WHERE book_id=:id", {"id":id}).fetchall()
    res = requests.get('https://www.goodreads.com/book/review_counts.json', params={"key": "ZyAo40hfWUwQdWxktTmA", "isbns": str(book.isbn) })
    data = res.json()

    goodreadratings=data['books'][-1]
    average_rating = goodreadratings['average_rating']
    total_reviews = goodreadratings["work_ratings_count"]


    return render_template('aboutbook.html', book=book, review=review, average_rating=average_rating, total_reviews=total_reviews)

@app.route("/rate", methods=["POST"])
def rate():
    now=datetime.datetime.now()
    year=now.year
    month=now.month
    day=now.day
    book_id=request.form.get('book_id')
    isbn=request.form.get('isbn')
    rating = request.form.get('rating')
    review = request.form.get('review')
    today=f"{year}-{month}-{day}"
    db.execute("INSERT INTO bookreviews (rating, review, date, book_id) VALUES (:rating, :review, :today, :book_id)", {"rating":rating, "review":review, "today": today, "book_id":book_id})
    db.commit()
     
       
    return render_template('error.html',message="Success")
    

@app.route("/api/<string:isbn>")

def detailedbook(isbn):
    book = db.execute("SELECT * FROM usertable WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    if book:
        
        return jsonify(
            {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": 28,
        "average_score": 5.0
    }
        )
    else:
        return jsonify({"error": "No such book"}),422


@app.route("/news")
def justy():
    user_id = session.get("user_id")
    return render_template('error.html', message = user_id)
    



        
        
            
        
    




