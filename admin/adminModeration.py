from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
import time

@app.route('/adminPanel/moderation')
def adminModeration():
    if 'admin' in session:
        adminName = session.get('admin')
        usersCount = getUsersCount()
    else:
        return redirect(url_for('adminLogin'))
    return render_template('adminUsers.html',adminName=adminName,usersCount=usersCount)

def getUsersCount():
    cursor.execute("SELECT COUNT(*) FROM users;")
    users = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM banned_users;")
    bannedUsers = cursor.fetchone()
    return users,bannedUsers