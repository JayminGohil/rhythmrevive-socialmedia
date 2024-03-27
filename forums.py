from flask import Flask, render_template, request, redirect, url_for, session
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
import checkBan

@app.route('/forums',methods=['GET','POST'])
def forums():
    if 'loginUsername' in session:
        userDbData = getUserData(session['loginUsername'])
        userUserId = userDbData[0]
        userUserName = userDbData[1]
        userRealName = userDbData[3]
        userPfpPath = userDbData[7]
        banStatus = checkBan.checkBan(userUserName)
        if banStatus:
            return redirect(url_for('banned'))
        if request.method == 'POST':
            forumInput = request.form['forumInput']
            saveForumToDatabase(userUserId,forumInput)
            msg = "Forum Uploaded Successfully!"
            return render_template('forums.html',userPfpPath=userPfpPath,userUserId=userUserId,msg=msg)
    else:
        return redirect(url_for('login'))
    return render_template('forums.html',userPfpPath=userPfpPath,userUserId=userUserId)


@app.route('/forums/<int:df_id>',methods=['GET','POST'])
def singleForums(df_id):
    if 'loginUsername' in session:
        userDbData = getUserData(session['loginUsername'])
        userUserId = userDbData[0]
        userUserName = userDbData[1]
        userRealName = userDbData[3]
        userPfpPath = userDbData[7]
        forum = fetchForum(df_id)
        if forum == []:
            return render_template('404forum.html',userPfpPath=userPfpPath,userUserId=userUserId)
        forumComments = fetchForumComments(df_id)
        forum = forum[0]
        if request.method == 'POST':
            forumComment = request.form['forumComment']
            saveForumCommentToDatabase(df_id,userUserId,forumComment)
            msg = "Comment Posted Successfully!"
            forumComments = fetchForumComments(df_id)
            return render_template('singleForum.html',userPfpPath=userPfpPath,userUserId=userUserId,msg=msg,forum=forum,forumComments=forumComments)
    else:
        return redirect(url_for('login'))
    return render_template('singleForum.html',userPfpPath=userPfpPath,userUserId=userUserId,forum=forum,forumComments=forumComments)

def fetchForum(df_id):
    cursor.execute("""
        SELECT d.df_id, d.user_id, d.title, d.creation_timestamp, u.user_name, u.user_pfp 
        FROM discussion_forums d 
        INNER JOIN users u ON d.user_id = u.user_id 
        WHERE d.df_id = %s;
    """, (df_id,))
    result = cursor.fetchall()
    return result

def fetchForumComments(df_id):
    cursor.execute("""
        SELECT d.df_cmnt_id, d.df_id, d.user_id, d.comment, d.comment_timestamp, u.user_name, u.user_pfp 
        FROM discussion_forums_comments d 
        INNER JOIN users u ON d.user_id = u.user_id 
        WHERE d.df_id = %s
        ORDER BY d.df_cmnt_id DESC;
    """, (df_id,))
    result = cursor.fetchall()
    return result


def getUserData(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    return result


def saveForumToDatabase(userid,forumInput):
    cursor.execute("INSERT INTO discussion_forums(user_id,title,creation_timestamp) VALUES(%s,%s,now())",(userid,forumInput,))
    conn.commit()

def saveForumCommentToDatabase(df_id,user_id,forumComment):
    cursor.execute("INSERT INTO discussion_forums_comments(df_id,user_id,comment,comment_timestamp) VALUES(%s,%s,%s,now())",(df_id,user_id,forumComment,))
    conn.commit()