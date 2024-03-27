from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
from datetime import datetime

@app.route('/fetch-posts', methods=['GET','POST'])
def fetchPosts():
    start_from = request.args.get('start_from', default=0, type=int)
    batch_size = 5
    current_user_id = request.args.get('current_user_id', type=int)

    cursor.execute("""
        SELECT p.post_id, p.user_id, p.caption, p.media_url, p.media_type, p.timestamp, u.user_name, u.user_pfp,
               (SELECT COUNT(*) FROM likes WHERE post_id = p.post_id) AS like_count,
               (SELECT COUNT(*) FROM comments WHERE post_id = p.post_id) AS comment_count,
               EXISTS (SELECT 1 FROM likes WHERE post_id = p.post_id AND user_id = %s) AS liked_by_user
        FROM posts p
        INNER JOIN users u ON p.user_id = u.user_id
        ORDER BY p.post_id DESC
        LIMIT %s OFFSET %s
    """, (current_user_id, batch_size, start_from))
    posts = cursor.fetchall()

    if posts:
        formatted_posts = [{
            'post_id': post[0],
            'user_id': post[1],
            'caption': post[2],
            'media_url': post[3],
            'media_type': post[4],
            'timestamp': post[5],
            'user_name': post[6],
            'user_pfp': post[7],
            'like_count': post[8],
            'comment_count': post[9],
            'liked_by_user': post[10]
        } for post in posts]
        return jsonify({'posts': formatted_posts})
    else:
        return jsonify({'posts': []})

@app.route('/fetch-lessons', methods=['GET','POST'])
def fetchLessons():
    start_from = request.args.get('start_from', default=0, type=int)
    batch_size = 5

    cursor.execute("""
        SELECT l.lesson_id, l.user_id, l.caption, l.media_url, l.media_type, l.timestamp, l.approval_status, u.user_name, u.user_pfp FROM lessons l
        INNER JOIN users u ON l.user_id = u.user_id
        ORDER BY l.lesson_id DESC
        LIMIT %s OFFSET %s
    """, (batch_size, start_from))
    posts = cursor.fetchall()
    print(posts)
    if posts:
        formatted_lessons = [{
            'lesson_id': post[0],
            'user_id': post[1],
            'caption': post[2],
            'media_url': post[3],
            'media_type': post[4],
            'timestamp': post[5],
            'approval_status': post[6],
            'user_name': post[7],
            'user_pfp' : post[8]
        } for post in posts]
        return jsonify({'lessons': formatted_lessons})
    else:
        return jsonify({'lessons': []})

@app.route('/fetch-sheet', methods=['GET','POST'])
def fetchSheet():
    start_from = request.args.get('start_from', default=0, type=int)
    batch_size = 5

    cursor.execute("""
        SELECT s.sheet_id, s.user_id, s.caption, s.media_url, s.media_type, s.timestamp, s.approval_status, u.user_name, u.user_pfp FROM sheet_music s
        INNER JOIN users u ON s.user_id = u.user_id
        ORDER BY s.sheet_id DESC
        LIMIT %s OFFSET %s
    """, (batch_size, start_from))
    posts = cursor.fetchall()
    print(posts)
    if posts:
        formatted_lessons = [{
            'sheet_id': post[0],
            'user_id': post[1],
            'caption': post[2],
            'media_url': post[3],
            'media_type': post[4],
            'timestamp': post[5],
            'approval_status': post[6],
            'user_name': post[7],
            'user_pfp' : post[8]
        } for post in posts]
        return jsonify({'lessons': formatted_lessons})
    else:
        return jsonify({'lessons': []})
    
@app.route('/fetch-forums', methods=['GET','POST'])
def fetchForums():
    start_from = request.args.get('start_from', default=0, type=int)
    batch_size = 5

    cursor.execute("""
        SELECT d.df_id, d.user_id, d.title, d.creation_timestamp,u.user_name, u.user_pfp FROM discussion_forums d
        INNER JOIN users u ON d.user_id = u.user_id
        ORDER BY d.df_id DESC
        LIMIT %s OFFSET %s
    """, (batch_size, start_from))
    posts = cursor.fetchall()
    print(posts)
    if posts:
        formatted_forums = [{
            'df_id': post[0],
            'user_id': post[1],
            'title': post[2],
            'creation_timestamp': post[3],
            'user_name': post[4],
            'user_pfp' : post[5]
        } for post in posts]
        return jsonify({'forums': formatted_forums})
    else:
        return jsonify({'forums': []})
    
@app.route('/post/<int:post_id>', methods=['GET','POST'])
def post(post_id):
    if 'loginUsername' in session:
        userDbData = getUserData(session['loginUsername'])
        userUserId = userDbData[0]
        userUserName = userDbData[1]
        userRealName = userDbData[3]
        userPfpPath = userDbData[7]
        post = loadPost(userUserId,post_id)
        comments = loadPostComments(post_id)
        if post == None:
            return render_template('404post.html',userPfpPath=userPfpPath,userUserId=userUserId)
        print(post)
        if request.method == 'POST':
            postComment = request.form['post-comment']
            insertCommentInDatabase(userUserId,post_id,postComment)
            post = loadPost(userUserId,post_id)
            comments = loadPostComments(post_id)
            return render_template('singlePost.html',userPfpPath=userPfpPath,userUserId=userUserId,post=post,comments=comments)
    else:
        return redirect(url_for('login'))
    return render_template('singlePost.html',userPfpPath=userPfpPath,userUserId=userUserId,post=post,comments=comments)

def getUserData(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    return result

def loadPost(user_id,post_id):
    cursor.execute("""
        SELECT p.post_id, p.user_id, p.caption, p.media_url,p.media_type,p.timestamp,u.user_name, u.user_pfp,
        (SELECT COUNT(*) FROM likes WHERE post_id = p.post_id) AS like_count,
        (SELECT COUNT(*) FROM comments WHERE post_id = p.post_id) AS comment_count,
        EXISTS (SELECT 1 FROM likes WHERE post_id = p.post_id AND user_id = %s) AS liked_by_user
        FROM posts p
        INNER JOIN users u ON p.user_id = u.user_id WHERE p.post_id=%s
    """, (user_id,post_id,))
    post = cursor.fetchone()
    return post

def loadPostComments(post_id):
    cursor.execute("""
        SELECT c.comment_id,c.user_id,c.post_id,c.comment_text,c.comment_timestamp,u.user_name, u.user_pfp
        FROM comments c
        INNER JOIN users u ON c.user_id = u.user_id
        WHERE post_id=%s ORDER BY c.comment_id DESC
    """, (post_id,))
    comments = cursor.fetchall()
    return comments

def insertCommentInDatabase(user_id,post_id,comment_text):
    cursor.execute("INSERT INTO comments(user_id, post_id, comment_text, comment_timestamp) VALUES (%s, %s, %s,NOW())",(user_id, post_id, comment_text,))
    conn.commit()