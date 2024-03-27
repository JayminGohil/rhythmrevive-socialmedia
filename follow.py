from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from rhythmrevive import app
from sqlconnect import conn,cursor

@app.route('/followUser/<self_id>+<user_id>')
def followUser(self_id,user_id):
    selfUserId = self_id
    otherUserId = user_id
    print(selfUserId,otherUserId)
    if isFollowingFn(selfUserId,otherUserId):
        return 'Already Following!'
    else:
        try:
            followUserFn(selfUserId,otherUserId)
            return 'User Followed!'
        except Exception as e:
            return 'Error In User Follow.'


def followUserFn(source,target):
    cursor.execute("INSERT INTO followers(source_user_id,target_user_id,follow_timestamp) VALUES(%s,%s,now())", (source,target,))
    conn.commit()

def isFollowingFn(selfuserid,otheruserid):
    cursor.execute("SELECT * FROM followers WHERE source_user_id = %s and target_user_id = %s", (selfuserid,otheruserid,))
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False

@app.route('/unfollowUser/<self_id>+<user_id>')
def unfollowUser(self_id,user_id):
    selfUserId = self_id
    otherUserId = user_id
    print(selfUserId,otherUserId)
    try:
        unfollowUserFn(selfUserId,otherUserId)
        return 'User Unfollowed!'
    except Exception as e:
        return 'Error In User Unfollow.'


def unfollowUserFn(source,target):
    cursor.execute("DELETE FROM followers WHERE source_user_id=%s AND target_user_id=%s", (source,target,))
    conn.commit()

@app.route('/getFollowers/<user_id>')
def getFollowers(user_id):
    cursor.execute("SELECT COUNT(*) FROM followers WHERE target_user_id = %s", (user_id,))
    result = cursor.fetchone()
    follower_count = result[0] if result else 0
    return str(follower_count)