# _*_ coding: utf-8 _*_
from flask import Flask, render_template, session, request, redirect, g
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)
DATABASE = 'test.db'

#db functions
def init_db():
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    tb_lst = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if(tb_lst == None):
        cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, userid VARCHAR(12) NOT NULL, pwd TEXT NOT NULL, email TEXT NOT NULL, real_name TEXT);")
        print("> Create user table Sucess.")
    cur.commit()
    cur.close()
    db.close()
    
@app.route('/')
def index():
    if session.get("account_id") is not None:
        return render_template('signup.html')
    else :
        return render_template('login.html')

# login function
@app.route('/account/login')
def login():
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]
    '''
    @TODO : db connect and compare user id and pw
    디비에서 받아온 user_id와 pw 를 꼭 변수로 받아 둘 것!!
    '''
    flag = cur.execute("SELECT EXISTS (SELECT * FROM user WHERE userid = '%s' AND pwd = '%s');")
    if flag == 1:
        return [user_id, user_pw]
    else:
        return
    
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
    user_em = request.form["user_email"]
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