from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
import time

@app.route('/adminPanel/posts', methods=['GET', 'POST'])
def adminPosts():
    if 'admin' in session:
        adminName = session.get('admin')
        posts = getPendingLessons()
        if request.method == 'POST':
            lesson_id = request.form['hidden-id']
            if request.form.get('approve-lesson'):
                status = "approved"
                updateLessonStatus(lesson_id,status)
                msg = "Lesson Was Approved!"
                posts = getPendingLessons()
                return render_template('adminPosts.html',posts=posts,adminName=adminName,msg=msg)
            elif request.form.get('reject-lesson'):
                status = "declined"
                updateLessonStatus(lesson_id,status)
                msg = "Lesson Was Rejected!"
                posts = getPendingLessons()
                return render_template('adminPosts.html',posts=posts,adminName=adminName,msg=msg)
        return render_template('adminPosts.html',posts=posts,adminName=adminName)
    else:
        return redirect(url_for('adminLogin'))

def getPendingLessons():
    cursor.execute("""SELECT l.lesson_id, l.user_id, l.caption, l.media_url, l.timestamp, u.user_name, u.       user_pfp 
        FROM lessons l
        JOIN users u ON l.user_id = u.user_id
        WHERE l.approval_status = 'pending';""",)
    result = cursor.fetchall()
    return result

def updateLessonStatus(lesson_id,status):
    cursor.execute("UPDATE lessons SET approval_status=%s WHERE lesson_id=%s",(status,lesson_id))
    conn.commit()