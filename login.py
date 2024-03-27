from flask import Flask, render_template, request, redirect, url_for, session
from rhythmrevive import app
from sqlconnect import conn,cursor
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginmsg_list = ["Registration Complete! You Can Now Login", "Password Reset Successful!"]
    loginmsg = request.args.get('loginmsg')
    loginError = request.args.get('loginError')
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        if doUserExist(username):
            print("Username Found In Database!", username)
            storedEncPass = getUserPassword(username)[0]
            print("Password In Database : ",storedEncPass)
            inputEncPass = generate_password_hash(password, method='scrypt')
            print("Password User Entered : ",inputEncPass)
            print(check_password_hash(storedEncPass, password))
            if check_password_hash(storedEncPass, password):
                print("Login Successful For User : ",username)
                session.permanent = True
                session['loginUsername'] = username
                return redirect(url_for('index'))
            else:
                return render_template('login.html',loginError="Password Is Incorrect!")
        else:
            return render_template('login.html',loginError="Username Is Invalid!")
    return render_template('login.html',loginError=loginError,loginmsg=loginmsg)

def doUserExist(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
    
def getUserPassword(username):
    cursor.execute("SELECT user_pass FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    print(result)
    return result

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

