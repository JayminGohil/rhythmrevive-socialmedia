from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
import time
import os
import json

@app.route('/adminPanel/badges', methods=['GET', 'POST'])
def adminBadges():
    if 'admin' in session:
        adminName = session.get('admin')
        allBadges = getAllBadges()
        print(allBadges)
        if request.method == 'POST':
            if 'addBadge' in request.form:
                badgeName = request.form['badgeName']
                badgeDesc = request.form['badgeDesc']
                badgePhoto = request.files.get('badgePhoto')
                if badgePhoto:
                    filename = badgePhoto.filename
                    storage_folder = "./static/storage/badges"
                    media_path = os.path.join(storage_folder, filename)
                    badgePhoto.save(media_path)
                    media_path = '.' + media_path
                    addBadgeToDatabase(badgeName, media_path, badgeDesc)
                    allBadges = getAllBadges()
                    msg = "Badge Added To The Server!"
                    return render_template('adminBadges.html',allBadges=allBadges,adminName=adminName,msg=msg)
            elif 'awardSubmit' in request.form:
                hiddenUsername = request.form['hiddenUsername']
                awardBadge = request.form['awardBadge']
                print(hiddenUsername, awardBadge)
                userBadgesString = getUserBadges(hiddenUsername)[0]
                userBadges  = json.loads(userBadgesString)
                if awardBadge in userBadges[0]:
                    print('User Already Has That Badge!')
                    msg = "User Already Has That Badge!"
                    return render_template('adminBadges.html',allBadges=allBadges,adminName=adminName,msg=msg)
                else:
                    userBadges[0][awardBadge] = 'notequipped'
                    print(userBadges)
                    updatedBadges = json.dumps(userBadges)
                    updateUserBadges(hiddenUsername,updatedBadges)
                    msg = "User Was Awarded With The Badge!"
                    return render_template('adminBadges.html',allBadges=allBadges,adminName=adminName,msg=msg)
        return render_template('adminBadges.html',allBadges=allBadges,adminName=adminName)
    else:
        return redirect(url_for('adminLogin'))


def addBadgeToDatabase(badgeName,media_path,badgeDesc):
    cursor.execute("INSERT INTO badges(badge_name,badge_url,badge_desc) VALUES(%s,%s,%s)",(badgeName,media_path,badgeDesc,))
    conn.commit()

def getAllBadges():
    cursor.execute("SELECT * FROM badges")
    result = cursor.fetchall()
    return result

def getUserBadges(username):
    cursor.execute("select user_badges FROM users WHERE user_name=%s",(username,))
    result = cursor.fetchone()
    return result

def updateUserBadges(username,updatedBadges):
    cursor.execute("UPDATE users SET user_badges=%s WHERE user_name=%s",(updatedBadges,username,))
    conn.commit()