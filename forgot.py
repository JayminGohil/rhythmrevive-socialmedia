from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mail import Mail, Message
from rhythmrevive import app,mail
from sqlconnect import conn,cursor
from werkzeug.security import generate_password_hash, check_password_hash
import secrets,datetime


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgotpass():
    if request.method == 'POST':
        useremail = request.form['useremail']
        if doEmailExist(useremail):
            token = secrets.token_urlsafe(50)
            print(token)
            session['pass_reset_session'] = {
                'token': token,
                'email': useremail,
            }
            subject = f'Rhythmrevive Password Reset Link'
            html_body = render_template('reset-password-mail.html')
            recipients = [useremail]
            message = Message(subject, recipients=recipients, html=html_body)
            try:
                mail.send(message)
                print("Mail Sent")
                return render_template('forgot.html',forgotError='Reset Link Sent')
            except Exception as e:
                print("Mail Not Sent")
                return render_template('forgot.html',forgotError='Mail Sending Error! Try again.')
        else:
            return render_template('forgot.html',forgotError='Email Address Not Found')
    return render_template('forgot.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if 'pass_reset_session' in session:
        if session['pass_reset_session']['token'] == token:
            if request.method == 'POST':
                newpass = request.form['newpass']
                encNewPass = generate_password_hash(newpass, method='scrypt')
                resetPassword(encNewPass,session['pass_reset_session']['email'])
                session.pop('pass_reset_session')
                print(f"Password reset successfully!")
                return redirect(url_for('login', loginmsg="Password Reset Successful!"))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    return render_template('reset-password.html')


def doEmailExist(email):
    cursor.execute("SELECT * FROM users WHERE user_email = %s", (email,))
    result = cursor.fetchone()    
    if result:
        return True
    else:
        return False

def resetPassword(newpassword,email):
    cursor.execute("UPDATE users SET user_pass = %s WHERE user_email = %s ", (newpassword,email,))
