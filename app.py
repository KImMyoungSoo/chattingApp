# _*_ coding: utf-8 _*_
from flask import Flask, render_template, session, request, redirect, g
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)
DATABASE = 'test.db'

def get_login(userid, pwd):
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    res = cur.execute("SELECT EXISTS (SELECT * FROM user WHERE userid='%s' AND pwd = '%s' AS SUCCESS", userid, pwd)
    db.commit()
    cur.close()
    db.close()
    if res == 1:
        return True
    else:
        return False

    
def check_db(db_name):
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    flag = cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='?';", db_name)
    if flag == 1:
        return True
    else:
        return False
    
@app.route('/')
def index():
    if session.get("account_id") is not None:
        return render_template('signup.html')
    else :
        return render_template('login.html')

# login function
@app.route('/account/login')
def login():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]

    db = sqlite3.connect("test.db")
    cur = db.cursor()
    '''
    @TODO : db connect and compare user id and pw
    '''
    # session['account_id'] = 
    '''
    @TODO : session create with db
    '''
    return redirect('/', code=302)

@app.route('/account/login')
def login():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]

    '''
    @TODO : db connect and compare user id and pw
    '''
    # session['account_id'] = 
    '''
    @TODO : session create with db
    '''
    return redirect('/', code=302)

@app.route('/account/signup', methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route('/account/create', methods=["POST"])
def create():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]
    user_em = request.form["user.email"]
    user_name = request.form["user_name"]
    db = sqlite3.connect()
    cur = db.cursor()
    cur.execute("INSERT INTO user(userid, pwd, email, name) VALUES(?, ?, ?, ?)", user_id, user_pw, user_em, user_name)
    cur.commit()
    cur.close()
    db.close()
    return redirect('/', code=302)

#app start
if __name__ == '__main__':
    socketio.run(app, port=9001, debug=True)