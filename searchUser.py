from flask import Flask, render_template, request, redirect, url_for, session,flash,jsonify
from rhythmrevive import app
from sqlconnect import conn,cursor
from flask import jsonify


@app.route('/searchUsers', methods=['GET', 'POST'])
def searchUsers():   
    query = request.args.get('query')
    if not query.strip():
        return []
    cursor.execute("SELECT user_name, display_name, user_pfp FROM users WHERE user_name LIKE %s OR display_name LIKE %s",('%' + query + '%', '%' + query + '%'))
    search_results = cursor.fetchall()
    print(search_results)
    return [{'username': row[0], 'name': row[1], 'profilePicture': row[2]} for row in search_results]

@app.route('/searchFullUsers', methods=['GET', 'POST'])
def searchFullUsers():   
    query = request.args.get('query')
    if not query.strip():
        return []
    cursor.execute("SELECT user_name, display_name,user_email, user_pfp,user_creation_timestamp,user_id FROM users WHERE user_name LIKE %s OR display_name LIKE %s",('%' + query + '%', '%' + query + '%'))
    search_results = cursor.fetchall()
    print(search_results)
    return [{'username': row[0], 'name': row[1],'useremail': row[2], 'profilePicture': row[3],'timestamp': row[4],'userid': row[5]} for row in search_results]


@app.route('/searchBannedUsers', methods=['GET'])
def search_banned_users():
        query = request.args.get('query')
        if not query.strip():
            return []
        cursor.execute("SELECT ban_id, user_id, user_name, user_email, banTimestamp,banReason FROM banned_users WHERE user_name LIKE %s OR user_email LIKE %s", ('%' + query + '%', '%' + query + '%'))
        search_results = cursor.fetchall()
        print(search_results)
        return [{'ban_id': row[0], 'user_id': row[1],'user_name': row[2], 'user_email': row[3],'banTimestamp': row[4],'banReason': row[5]} for row in search_results]


@app.route('/banUser', methods=['POST'])
def banUser():
    if request.method == 'POST':
        data = request.json
        user_id = data.get('userId')
        if checkUserBan(user_id):
            return jsonify({'message': 'User Already Banned'}), 200
        banReason = data.get('banReason')
        print(user_id,banReason)
        user_name = getUserDataWithId(user_id)[0]
        user_email = getUserDataWithId(user_id)[1]
        banUser(user_id,user_name,user_email,banReason)
        return jsonify({'message': 'User banned successfully'}), 200
    else:
        return jsonify({'error': 'Method not allowed'}), 405


def getUserDataWithId(user_id):
    cursor.execute("SELECT user_name,user_email FROM users WHERE user_id=%s",(user_id,))
    result = cursor.fetchone()
    return result

def banUser(user_id,user_name,user_email,banReason):
    cursor.execute("INSERT INTO banned_users(user_id,user_name,user_email,banTimestamp,banReason) VALUES(%s,%s,%s,NOW(),%s)",(user_id,user_name,user_email,banReason))
    conn.commit()

def checkUserBan(user_id):
    cursor.execute("SELECT * FROM banned_users WHERE user_id=%s",(user_id,))
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False
    

@app.route('/unban', methods=['POST'])
def unban_user():
    try:
        ban_id = request.form.get('ban_id')
        print(ban_id)
        unbanDb(ban_id)
        return jsonify({'message': 'User successfully unbanned'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def unbanDb(ban_id):
    cursor.execute("DELETE FROM banned_users WHERE ban_id=%s",(ban_id,))
    conn.commit()