from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
import time

@app.route('/adminPanel')
def adminPanel():
    if 'admin' in session:
        adminName = session.get('admin')
        print(adminName)
        userdata = getUserData()
        todayUsers = userdata[0][0]
        weekUsers = userdata[1][0]
        monthUsers = userdata[2][0]
        postdata = getPostData()
        todayPosts = postdata[0][0]
        weekPosts = postdata[1][0]
        monthPosts = postdata[2][0]
    else:
        return redirect(url_for('adminLogin'))
    return render_template('adminIndex.html',todayUsers=todayUsers,weekUsers=weekUsers,monthUsers=monthUsers,todayPosts=todayPosts,weekPosts=weekPosts,monthPosts=monthPosts,adminName=adminName)


def getUserData():
    cursor.execute("SELECT COUNT(*) FROM users WHERE DATE(user_creation_timestamp) = CURDATE();")
    today = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM users WHERE YEARWEEK(user_creation_timestamp) = YEARWEEK(NOW());")
    week = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM users WHERE YEAR(user_creation_timestamp) = YEAR(CURRENT_DATE) AND MONTH(user_creation_timestamp) = MONTH(CURRENT_DATE);")
    month = cursor.fetchone()
    return today,week,month

def getPostData():
    cursor.execute("SELECT COUNT(*) FROM posts WHERE DATE(timestamp) = CURDATE();")
    today = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM posts WHERE YEARWEEK(timestamp) = YEARWEEK(NOW());")
    week = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM posts WHERE YEAR(timestamp) = YEAR(CURRENT_DATE) AND MONTH(timestamp) = MONTH(CURRENT_DATE);")
    month = cursor.fetchone()
    return today,week,month

@app.route('/ping')
def ping():
    return jsonify(timestamp=time.time())