from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import random
import time
from rhythmrevive import app, mail
from sqlconnect import conn,cursor
from werkzeug.security import generate_password_hash, check_password_hash
import json

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    print(session)
    current_timestamp = int(time.time())
    if session.get('user_data',False):
        expiretimestamp = session.get('user_data').get('expiretimestamp')
       
        if current_timestamp>=expiretimestamp:
            print('session expired')
            session.pop('user_data')
            return redirect(url_for('register'))
          
    if 'user_data' in session:
        
        print(session['user_data'])
        global user_data
        user_data = session['user_data']
        print(user_data)
        email = user_data['email']
        name = user_data['name']
        password = user_data['password']
        user_otp = user_data['user_otp']
        username = user_data['username']
        
        if request.method == 'POST':
            userInputOTP = int(request.form['userOTP'])
            sentOTP = int(user_otp)
            
            print(f'User has submitted OTP : {userInputOTP}') 
            print(f'System has sent OTP : {sentOTP}') 

            encPass = generate_password_hash(password, method='scrypt')
            
            if userInputOTP == sentOTP:
                print("Valid OTP")
                with open('defaultBadges.json', 'r') as f:
                    default_badges = json.load(f)
                cursor.execute("INSERT INTO users(user_name, user_pass, display_name, user_email,user_creation_timestamp,user_badges) VALUES (%s, %s, %s, %s, NOW(),%s)",(username, encPass, name, email,json.dumps(default_badges)))
                conn.commit()

                subject = f'Welcome to RhythmRevive - Your Registration is Complete!'
                html_body = render_template('successMail.html')
                recipients = [email]
                message = Message(subject, recipients=recipients, html=html_body)
                try:
                    mail.send(message)
                    print("Mail Sent")
                except Exception as e:
                    print("Mail Not Sent")

                session.pop('user_data')
                return redirect(url_for('login',loginmsg="Registration Complete! You Can Now Login"))
            else:
                print("Invalid OTP")
                return render_template('verify.html',otpError="OTP is Invalid.")
    else:
        return redirect(url_for('register'))
      
    return render_template('verify.html')

@app.route('/resendOTP', methods=['GET', 'POST'])
def resendOTP():
    email = user_data['email']
    name = user_data['name']
    password = user_data['password']
    username = user_data['username']
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

    return render_template('resendOTP.html')

@app.route('/sessionExpired')
def sessionExpired():
    return render_template('sessionExpired.html')

if __name__ == '__main__':
    app.run(debug=True)