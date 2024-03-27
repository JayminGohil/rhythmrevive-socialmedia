from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
from app import socketio
from flask_socketio import emit,send
from datetime import datetime
import checkBan

@app.route('/messages/@<username>', methods=['GET', 'POST'])
def messagesUser(username):
    if 'loginUsername' in session:
        userDbData = getUserData(session['loginUsername'])
        userUserId = userDbData[0]
        userUserName = userDbData[1]
        userPfpPath = userDbData[7]
        banStatus = checkBan.checkBan(userUserName)
        if banStatus:
            return redirect(url_for('banned'))
        otherUserData = getUserData(username)
    else:
        return redirect(url_for('login'))
    return render_template('messageUser.html',userPfpPath=userPfpPath,userUserId=userUserId,otherUserData=otherUserData)

def getUserData(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    return result

@app.route('/fetch-messages', methods=['POST'])
def fetch_messages():
    data = request.json
    self_user_id = data['self_user_id']
    other_user_id = data['other_user_id']

    cursor.execute("""
        SELECT content, timestamp, sender_id
        FROM messages
        WHERE (sender_id = %s AND receiver_id = %s)
        OR (sender_id = %s AND receiver_id = %s)
        ORDER BY timestamp ASC
    """, (self_user_id, other_user_id, other_user_id, self_user_id))
    messages = cursor.fetchall()

    formatted_messages = [{
        'content': message[0],
        'timestamp': message[1].strftime('%Y-%m-%d %H:%M'),
        'sender_id': message[2]
    } for message in messages]

    return jsonify({'messages': formatted_messages})

