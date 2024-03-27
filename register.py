from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
import random
from rhythmrevive import app, mail
from sqlconnect import conn,cursor
import time

@app.route('/check_user_exists', methods=['POST'])
def check_user_exists():
    username = request.form['username']
    user_with_username = doUsernameExist(username)
    if user_with_username:
        return jsonify({'exists': True, 'message': 'Username Not Available'})
    else:
        return jsonify({'exists': False, 'message': 'User does not exist'})

@app.route('/check_email_exists', methods=['POST'])
def check_email_exists():
    email = request.form['email']
    user_with_email = doEmailExist(email)

    if user_with_email:
        return jsonify({'exists': True, 'message': 'Email already exists'})
    else:
        return jsonify({'exists': False, 'message': 'Email does not exist'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']

        if not name or not name.strip():
            return render_template('register.html', name_error='Name is required.')

        if not username or not username.strip():
            return render_template('register.html', username_error='Username is required.')

        if not email or not email.strip() or '@' not in email:
            return render_template('register.html', email_error='Invalid email address.')
        
        if doEmailExist(email) or doUsernameExist(username):
            if doEmailExist(email) and doUsernameExist(username):
                formError = 'Email & Username Already Exists'
            elif doEmailExist(email):
                formError = 'Email Already Exists'
            elif doUsernameExist(username):
                formError = 'Username Already Exists'
    
            return render_template('register.html', formError=formError)
        else:
            otp = random.randint(100000,999999)
            current_timestamp = int(time.time())
            timestamp_after_2_minutes = current_timestamp + 120
   
            session['user_data'] = {
                'name': name,
                'username': username,
                'email': email,
                'password': password,
                'user_otp' : otp,
                'expiretimestamp' : timestamp_after_2_minutes
            }   
            subject = f'Rhythmrevive OTP for {name} : {otp} '
            html_body = render_template('mail.html')
            recipients = [email]
            message = Message(subject, recipients=recipients, html=html_body)
            try:
                mail.send(message)
                print("Mail Sent")
            except Exception as e:
                print("Mail Not Sent")
            return redirect(url_for('verify'))

    return render_template('register.html')

def doEmailExist(email):
    cursor.execute("SELECT * FROM users WHERE user_email = %s", (email,))
    result = cursor.fetchone()    
    if result:
        return True
    else:
        return False
    
def doUsernameExist(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()    
    if result:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)
