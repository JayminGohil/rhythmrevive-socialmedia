from flask import Flask, render_template, request, redirect, url_for, session
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
import checkBan

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'loginUsername' in session:
        userDbData = getUserData(session['loginUsername'])
        userUserId = userDbData[0]
        userUserName = userDbData[1]
        userRealName = userDbData[3]
        userPfpPath = userDbData[7]
        banStatus = checkBan.checkBan(userUserName)
        if banStatus:
            return redirect(url_for('banned'))
        interacted_users = get_interacted_users(userUserId)
    else:
        return redirect(url_for('login'))
    return render_template('messages.html',userPfpPath=userPfpPath,userUserId=userUserId,interacted_users=interacted_users)

def getUserData(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    return result

def get_interacted_users(user_id):
    cursor.execute("""
        SELECT DISTINCT sender_id, receiver_id 
        FROM messages 
        WHERE receiver_id = %s OR sender_id = %s
    """, (user_id, user_id))
    
    interacted_user_ids = set()
    for row in cursor.fetchall():
        sender_id, receiver_id = row
        if sender_id != user_id:
            interacted_user_ids.add(sender_id)
        if receiver_id != user_id:
            interacted_user_ids.add(receiver_id)
    
    interacted_users = []
    for user_id in interacted_user_ids:
        cursor.execute("SELECT user_id, user_name, user_pfp FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            interacted_users.append(user_data)
    
    return interacted_users