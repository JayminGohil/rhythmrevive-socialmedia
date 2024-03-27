from flask import Flask, render_template, request, redirect, url_for, session
from rhythmrevive import app
from sqlconnect import conn,cursor
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if doAdminExist(username):
            print("Username Found In Database!", username)
            storedEncPass = getAdminPassword(username)[0]
            print("Password In Database : ",storedEncPass)
            inputEncPass = generate_password_hash(password, method='scrypt')
            print("Password User Entered : ",inputEncPass)
            print(check_password_hash(storedEncPass, password))
            if check_password_hash(storedEncPass, password):
                session.permanent = True
                session['admin'] = (username)
                return redirect(url_for('adminPanel'))
            else:
                return render_template('adminLogin.html',loginError="Password Is Incorrect!")
        else:
            return render_template('adminLogin.html',loginError="Username Is Invalid!")
    return render_template('adminLogin.html')



def doAdminExist(username):
    cursor.execute("SELECT * FROM admins WHERE admin_username = %s", (username,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
    
def getAdminPassword(username):
    cursor.execute("SELECT admin_password FROM admins WHERE admin_username = %s", (username,))
    result = cursor.fetchone()
    print(result)
    return result

@app.route('/adminLogout')
def adminLogout():
    session.pop('admin')
    return redirect(url_for('adminLogin'))