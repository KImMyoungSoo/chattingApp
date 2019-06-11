# _*_ coding: utf-8 _*_
from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, emit
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = "super secret key"
socketio = SocketIO(app)
DATABASE = 'test.db'

#db functions
def init_db():
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table';")
    tb_lst = cur.fetchone()[0]
    if(tb_lst == 0):
        print("> created DB")
        cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, userid VARCHAR(12) NOT NULL, pwd TEXT NOT NULL, email TEXT NOT NULL, username TEXT);")
        cur.execute("CREATE TABLE L_log(id INTEGER PRIMARY KEY AUTOINCREMENT, userid VARCHAR(12), real_nm VARCHAR(12), room_name TEXT NOT NULL, message TEXT NOT NULL, ts TIMESTAMP DEFAULT (datetime('now','localtime')));")
        cur.execute("CREATE TABLE P_log(id INTEGER PRIMARY KEY AUTOINCREMENT, s_user VARCHAR(12), r_user VARCHAR(12), message TEXT NOT NULL, ts TIMESTAMP DEFAULT(datetime('now','localtime')));")
        '''
        @TODO : 채팅방 채팅로그등 기능구현에 필요한 테이블 추가 생성
        '''
    db.commit()
    cur.close()
    db.close()
    
@app.route('/')
def index():
    if session.get("account_id") is not None:
        return render_template('rooms.html')
    else :
        return render_template('login.html')

# login function
@app.route('/account/login', methods=["POST"])
def login():
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]
    
    
    cur.execute("SELECT EXISTS (SELECT * FROM user WHERE userid = ? AND pwd = ?);", (user_id, user_pw))
    flag = cur.fetchone()[0]
    if flag == 1:
        session["account_id"] = user_id
        cur.execute("SELECT username FROM user WHERE userid = ?;", [user_id])
        session["user_id"] = cur.fetchone()
        print('> session : ' + session['account_id'])
        return redirect('/', code=302)
    else:
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
    
    db = sqlite3.connect('test.db')
    cur = db.cursor()
    cur.execute("INSERT INTO user(userid, pwd, email, username) VALUES(?, ?, ?, ?)", (user_id, user_pw, user_em, user_name))
    db.commit()
    cur.close()
    db.close()

    return redirect('/', code=302)

@app.route('/room1')
def rooms1():
    session['room'] = 'room1'
    print(">>> room session : " + session['room'])
    return render_template('index.html')

@app.route('/room2')
def rooms2():
    session['room'] = 'room2'
    print(">>> room session : " + session['room'])
    return render_template('index.html')

@app.route('/room3')
def rooms3():
    session['room'] = 'room3'
    print(">>> room session : " + session['room'])
    return render_template('index.html')

#Socketio Part

#connecting
@socketio.on('connect', namespace='/chat')
def connect():
    print("Connected ...")

#처음 채팅방에 들어왔을때
@socketio.on('first', namespace='/chat')
def test(data):
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    print(data)
    # print('-----------------')
    # account = session['account_id']
    # print(account)
    # print('-----------------')
    sess = str(session['user_id'])
    sess = sess[2:-3]
    print(sess)
    mes = sess + " 님 께서 입장하셨습니다."
    cur.execute("SELECT real_nm, room_name, message, ts FROM L_log WHERE room_name=? ORDER BY id ASC LIMIT 100",(session['room'],))
    last_message = cur.fetchall()
    for ms in last_message:
        username, roomname, msg, ts = ms
        sess = str(session['user_id'])
        sess = sess[2:-3]
        ty = None
        if username == sess :
            ty = 'me'
        else :
            ty = 'message'
        emit('makechat',{'room': session['room'], 'type': ty, 'name': username, 'message': msg, 'ts': ts})
        print(ms)
    '''
    @TODO : 기존의 로그를 불러올 수 있어야 함 모든 로그를 불러오면 많을수 있으므로 가장 최신의 몇개정도를 불러오는게 좋을듯 함
    '''
    db.commit()
    cur.close()
    db.close()
    emit('makechat',{'room': session['room'], 'type': 'connect', 'name': 'SERVER', 'message': mes, 'ts': str(datetime.datetime.now())} , broadcast = True)

# 유저가 입력한 message를 모두에게 전송
@socketio.on('message', namespace='/chat')
def message(data):
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    print(data)
    ty = data['type']
    msg = data['message']
    sess = str(session['user_id'])
    sess = sess[2:-3] # sess => user name 
    account = session['account_id'] # account => userid
    roomname = session['room']
    cur.execute("INSERT INTO L_log(userid, real_nm, message, room_name) VALUES(?, ?, ?, ?);",(account, sess, msg,roomname))
    db.commit()
    cur.close()
    db.close()
    now = datetime.datetime.now()
    tis = "%04d-%02d-%02d %02d:%02d:%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    '''
    @TODO : 채팅방 로그 생성 즉 데이터를 디비에 추가
    '''
    emit('makechat',{'room': session['room'], 'type': ty, 'name': sess, 'message': msg, 'ts': str(tis)}, broadcast = True, include_self=False)

@socketio.on('disconnect', namespace='/chat')
def disconnect():
    sess = str(session['user_id'])
    sess = sess[2:-3]
    mes = sess + " 님 께서 퇴장하셨습니다."
    now = datetime.datetime.now()
    tis = "%04d-%02d-%02d %02d:%02d:%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    emit('makechat',{'room': session['room'], 'type': 'disconnect', 'name': 'SERVER', 'message': mes, 'ts': str(tis)}, broadcast = True, include_self=False)

#app start
if __name__ == '__main__':
    init_db()
    socketio.run(app, port=9001, debug=True)