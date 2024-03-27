from flask import Flask,request,session,jsonify
import random
from sqlconnect import conn,cursor
from rhythmrevive import app


@app.route('/addlike/<int:myuserid>/<int:postid>', methods=['GET', 'POST'])
def addLike(myuserid, postid):
    if isLiked(myuserid,postid):
        print('Already Liked')
    else:
        try:
            likePostFn(myuserid,postid)
            return 'Post Liked!'
        except Exception as e:
            return 'Error In Post Like.'
        

@app.route('/removeLike/<int:myuserid>/<int:postid>', methods=['GET', 'POST'])
def removeLike(myuserid, postid):
    if isLiked(myuserid,postid):
        try:
            removeLikePostFn(myuserid,postid)
            return 'Post Like Removed!'
        except Exception as e:
            return 'Error In Post Like Removal.'
    else:
        return 'Not Liked'
    
@app.route('/fetchLikes/<int:postid>', methods=['GET', 'POST'])
def fetchLikes(postid):
    try:
        likes_count = fetchLikesFn(postid)
        return jsonify({'likes_count': likes_count})
    except Exception as e:
        return 'Error Fetching Likes'
    

def fetchLikesFn(postid):
    cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id = %s", (postid,))
    conn.commit()
    result = cursor.fetchone()[0]
    return result


def likePostFn(myuserid, postid):
    cursor.execute("INSERT INTO likes(user_id,post_id,like_timestamp) VALUES(%s,%s,now())", (myuserid,postid,))
    conn.commit()

def removeLikePostFn(myuserid, postid):
    cursor.execute("DELETE FROM likes WHERE user_id=%s and post_id=%s", (myuserid,postid,))
    conn.commit()

def isLiked(myuserid,postid):
    cursor.execute("SELECT * FROM likes WHERE user_id = %s and post_id = %s", (myuserid,postid,))
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False