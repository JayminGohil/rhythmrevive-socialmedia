from flask import Flask, render_template, request, redirect, url_for, session
import random
from sqlconnect import conn,cursor
from rhythmrevive import app

@app.route('/banned')
def banned():
    return render_template('banned.html')


def checkBan(username):
    cursor.execute("SELECT * FROM banned_users WHERE user_name=%s",(username,))
    result = cursor.fetchone()
    if result:
        print("Banned User")
        return True
    else:
        print("Not Banned")
        return False