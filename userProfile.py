from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from rhythmrevive import app
from sqlconnect import conn,cursor
import json
import checkBan

@app.route('/userProfile/')
@app.route('/userProfile/@<user_name>')
def userProfile(user_name=None):
    if 'loginUsername' in session:
        userDbData = getUserData(session['loginUsername'])
        selfUserId = userDbData[0]
        selfProfilePfp = userDbData[7]
        userUserName = userDbData[1]
        isFollowing = False
        if user_name is None or user_name==userUserName:
            selfProfile = True           
            userUserId = userDbData[0]
            userUserName = userDbData[1]
            userRealName = userDbData[3]
            userBio = userDbData[6]
            userPfpPath = userDbData[7]
            userInterests = userDbData[9]
            userCreation = userDbData[10]
            userFollowers = getFollowers(userUserId)[0]
            userFollowing = getFollowing(userUserId)[0]
            userBadges = json.loads(userDbData[8])[0]
            banStatus = checkBan.checkBan(userUserName)
            if banStatus:
                return redirect(url_for('banned'))
            equipBadge = getEquippedBadge(userBadges)
            if userBio == None:
                userBio = 'No bio set yet.'
            if userInterests == None:
                userInterests = 'No interests set yet.'
            userCreationInWords = convertUserCreationToWords(userCreation)
            userPosts = getUserPosts(userUserId)
            followers_info = getUserFollowersInfo(userUserId)
            followings_info = getUserFollowingInfo(userUserId)
        else:
            selfProfile = False
            userDbData = getUserData(user_name)
            if userDbData == None:
                return render_template('404user.html',user_name=user_name,selfProfilePfp=selfProfilePfp)
            userUserId = userDbData[0]
            userUserName = userDbData[1]
            userRealName = userDbData[3]
            userBio = userDbData[6]
            userPfpPath = userDbData[7]
            userInterests = userDbData[9]
            userCreation = userDbData[10]
            userFollowers = getFollowers(userUserId)[0]
            userFollowing = getFollowing(userUserId)[0]
            userBadges = json.loads(userDbData[8])[0]
            equipBadge = getEquippedBadge(userBadges)
            isFollowing = isFollowingFn(selfUserId,userUserId)
            if userBio == None:
                userBio = 'No bio set yet.'
            if userInterests == None:
                userInterests = 'No interests set yet.'
            userCreationInWords = convertUserCreationToWords(userCreation)
            userPosts = getUserPosts(userUserId)
            followers_info = getUserFollowersInfo(userUserId)
            followings_info = getUserFollowingInfo(userUserId)
    else:
        return redirect(url_for('login'))
    return render_template('userProfile.html',selfUserId=selfUserId,userUserId=userUserId,userPfpPath=userPfpPath,userUserName=userUserName,userRealName=userRealName,userFollowers=userFollowers,selfProfile=selfProfile,userBio=userBio,userInterests=userInterests,userCreationInWords=userCreationInWords,userPosts=userPosts,userFollowing=userFollowing,selfProfilePfp=selfProfilePfp,isFollowing=isFollowing,followers_info = followers_info,followings_info=followings_info,equipBadge=equipBadge)

           
def getUserData(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    print(result)
    return result

def getFollowers(userid):
    cursor.execute("SELECT COUNT(*) FROM followers WHERE target_user_id = %s", (userid,))
    result = cursor.fetchone()
    return result

def getFollowing(userid):
    cursor.execute("SELECT COUNT(*) FROM followers WHERE source_user_id = %s", (userid,))
    result = cursor.fetchone()
    return result

def convertUserCreationToWords(userCreation):
    current_time = datetime.now()
    time_difference = current_time - userCreation
    days_difference = time_difference.days
    if days_difference == 0:
        formatted_time = 'today'
    elif days_difference == 1:
        formatted_time = '1 day ago'
    else:
        formatted_time = f'{days_difference} days ago'
    return formatted_time

def getUserPosts(userid):
    cursor.execute("""
        SELECT 
            p.post_id,
            p.caption,
            p.media_url,
            p.media_type,
            COUNT(l.post_id) AS like_count,
            COUNT(c.post_id) AS comment_count
        FROM 
            posts p
        LEFT JOIN 
            likes l ON p.post_id = l.post_id
        LEFT JOIN 
            comments c ON p.post_id = c.post_id
        WHERE 
            p.user_id = %s
        GROUP BY 
            p.post_id
        ORDER BY 
            p.post_id DESC
    """, (userid,))
    result = cursor.fetchall()       
    return result

def getEquippedBadge(dictionary):
    search_value = 'equipped'
    for key, value in dictionary.items():
        if value == search_value:
            equipped = key
    cursor.execute("SELECT * FROM badges WHERE badge_name = %s", (equipped,))
    result = cursor.fetchone()
    return result


def isFollowingFn(selfuserid,otheruserid):
    cursor.execute("SELECT * FROM followers WHERE source_user_id = %s and target_user_id = %s", (selfuserid,otheruserid,))
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False
    
def getUserFollowersInfo(userid):
    cursor.execute("SELECT source_user_id FROM followers WHERE target_user_id = %s", (userid,))
    result = cursor.fetchall()
    result = [user_id[0] for user_id in result]
    print(result)
    
    followers_info = []
    
    for follower_id in result:
        cursor.execute("SELECT user_id, user_name, user_pfp FROM users WHERE user_id = %s", (follower_id,))
        follower_info = cursor.fetchone()
        followers_info.append(follower_info)
    
    print(followers_info)
    return followers_info

def getUserFollowingInfo(userid):
    cursor.execute("SELECT target_user_id FROM followers WHERE source_user_id = %s", (userid,))
    result = cursor.fetchall()
    result = [user_id[0] for user_id in result]
    print(result)
    
    followings_info = []
    
    for following_id in result:
        cursor.execute("SELECT user_id, user_name, user_pfp FROM users WHERE user_id = %s", (following_id,))
        following_info = cursor.fetchone()
        followings_info.append(following_info)
    
    print(followings_info)
    return followings_info