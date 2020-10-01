from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
#import socketio

from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key='secret'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

#socketio connect
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)



#Class created to hold each registered user's info
class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password

#Class to hold each message
class Chats():
    def __init__(self, msg, user):
        self.msg = msg
        self.user = user



#User holds details for each user
userss = []

#Created Chat Rooms
chatRooms = []

rt=['2','4','5']

# This is used to sign up each user
@app.route('/register')
def register():
    return render_template('registrr.html')

# This renders the page for user to input login details
@app.route('/login')
def login():
    return render_template('login.html')

#Logs in a user if detail is correct
@app.route('/logsin', methods=['POST'])
def logsin():
    username=request.form.get('username')
    password=request.form.get('password')

    #Check for user in existing list of users
    for user in userss:
        # If a user exist
        if user.username == username:
            #Check for password
            if user.password == password:
                #cREATE USER SESSION
                session['username'] = user.username
                session['password'] = user.password

                #Send user to homepage
                return redirect( url_for('homepage'))
            else:
                return render_template('error.html', error='incorrect password') #str(user.password)

    return 'no such user'
    
    
        


@app.route('/')
def use():
    return userss[1]

# To register a user
@app.route('/userInfo', methods=['POST'])
def adduser():
    username=str(request.form.get('username'))
    password=str(request.form.get('password'))
    password2=str(request.form.get('password2'))

    for user in userss:
        if user.username == username:
            return render_template('error.html', error='User already exist')
        
    if password == password2:
        user=User(username=username, password=password)
        userss.append(user)
        return render_template('login.html')
    else:
        return render_template('error.html', error='passwords do not match')

#Go to homepage
@app.route('/homepage')
def homepage():
    #Get user
    user = session.get('username')
    if user:
        #If a registered user is signed in, go to homepage.html
        return render_template('homepage.html', user=user, chatRooms=chatRooms)
    else:
        #Else
        return render_template('login.html')

#Look at when you wake
@socketio.on('createRoom')
def createRoom(data):
    user = session.get('username')
    if user:
        createChat = str(data['createChat'])
        msg = list(data['msg'])
        userprofile = user

        values = {'createChat': createChat, 'user': userprofile, 'msg': msg}
        
        #If chat Room already exist, return chat Room already exist
        for chatRoom in chatRooms:
            if chatRoom['createChat'] == createChat:
                return render_template('error.html', error='chatroom already exist')

        # If no such chatRoom exist, add chatRoom
        chatRooms.append(values)        
        
        # Use socketio to redirect user to created ChatRoom pass in chats as argument
        emit('redirect', {'url': url_for('new_view', chats=createChat)}, broadcast=True)
        

@app.route('/new_view/<string:chats>')        
def new_view(chats):
    user = session.get('username')
    if user:
        for room in chatRooms:
            if room['createChat'] == chats:
                return render_template('room.html', room=room, user=user)
        
    else:
        return render_template('login.html')


# When we get a message
@socketio.on('message')
def message(data):
    # {'msg': text, 'user': user}
    # {'createChat': createChat, 'user': userprofile, 'msg': msg}
    user = session.get('username')
    if user:
        createChat = str(data['createChat'])
        msg = str(data['msg'])
        user = str(data['user'])

        # If you want to add time, this is where you add it
        chat = {'msg': msg, 'user': user}

        for room in chatRooms:
            if room['createChat'] == createChat:
                room['msg'].append(chat)

                emit('sendMsg', {'room': room}, broadcast=True )


#  socket.emit('deletePost', {'msg': msg, 'user': user})
@socketio.on('deletePost')
def deletePost(data):
    user = session.get('username')
    if user:
        createChat = str(data['createChat'])
        msg = str(data['msg'])
        user = str(data['user'])

        for room in chatRooms:
            if room['createChat'] == createChat:
                for msgs in room['msg']:
                    if msgs['msg'] == msg:
                        if msgs['user'] == user:
                            room['msg'].remove(msgs)
                            emit('deleteMsg', {'room': room}, broadcast=True)















