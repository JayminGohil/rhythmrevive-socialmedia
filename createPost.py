from flask import Flask, render_template, request, redirect, url_for, session,flash
from rhythmrevive import app,mail
from sqlconnect import conn,cursor
import secrets
import os

@app.route('/createPost', methods=['GET', 'POST'])
def createPost():
    if 'loginUsername' in session:
        userDbData = getUserData(session['loginUsername'])
        userUserId = userDbData[0]
        userUserName = userDbData[1]
        userRealName = userDbData[3]
        userPfpPath = userDbData[7]
        if request.method == 'POST':
            postType = request.form['postType']
            postMedia = request.files.get('postMedia')
            postCaption = request.form['postCaption']

            if postMedia:
                allowed_extensions = set(['.jpg', '.jpeg', '.png', '.mkv', '.mp4'])
                filename = postMedia.filename
                allowed_image = set(['.jpg', '.jpeg', '.png'])
                allowed_video = set(['.mkv', '.mp4'])
                if not (filename.lower().endswith(extension) for extension in allowed_extensions):
                    fileError = 'Only the following file extensions are allowed: ' + ', '.join(allowed_extensions)
                    return render_template('createPost.html',fileError=fileError)
                unique_filename = secrets.token_urlsafe(60) + '.' + filename.split('.')[-1]

                for extension in allowed_extensions:
                    if filename.lower().endswith(extension):
                        if extension in allowed_image:
                            storage_folder = './static/storage/posts/photos'
                            media_type = 'photo'
                        else:
                            storage_folder = './static/storage/posts/videos'
                            media_type = 'video'
                        break
                media_path = os.path.join(storage_folder, unique_filename)

                try:
                    postMedia.save(media_path)

                except Exception as e:
                    print('Error saving file: ' + str(e))
                    fileError = 'File Upload Failed! Try Again.'
                    return render_template('createPost.html',fileError=fileError)
                # print(postType,unique_filename,media_path,postCaption,media_type)
                media_path = '.' + media_path
                if postType == 'post':
                    addPostToDb(userUserId,postCaption,media_path,media_type)
                    return render_template('createPost.html',fileError='Post Uploaded!',userPfpPath=userPfpPath)
                elif postType == 'video':
                    if media_type == 'video':
                        addLessonToDb(userUserId,postCaption,media_path,media_type)
                        return render_template('createPost.html',fileError='Video Lesson Uploaded!',userPfpPath=userPfpPath)
                    else:
                        return render_template('createPost.html',fileError='Can Not Upload Photos In Video Lessons!',userPfpPath=userPfpPath)
                elif postType == 'sheet':
                    if media_type == 'photo':
                        addSheetMusicToDb(userUserId,postCaption,media_path,media_type)
                        return render_template('createPost.html',fileError='Sheet Music Uploaded!',userPfpPath=userPfpPath)
                    else:
                        return render_template('createPost.html',fileError='Can Not Upload Videos In Sheet Music!',userPfpPath=userPfpPath)
    else:
        return redirect(url_for('login'))
    return render_template('createPost.html',userPfpPath=userPfpPath)

def getUserData(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    return result


def addPostToDb(uid,caption,url,type):
    cursor.execute("INSERT INTO posts(user_id, caption, media_url, media_type,timestamp) VALUES (%s, %s, %s, %s, NOW())",(uid, caption, url, type,))
    conn.commit()

def addLessonToDb(uid,caption,url,type):
    cursor.execute("INSERT INTO lessons(user_id, caption, media_url, media_type,timestamp,approval_status) VALUES (%s, %s, %s, %s, NOW(),'pending')",(uid, caption, url, type,))
    conn.commit()

def addSheetMusicToDb(uid,caption,url,type):
    cursor.execute("INSERT INTO sheet_music(user_id, caption, media_url, media_type,timestamp,approval_status) VALUES (%s, %s, %s, %s, NOW(),'approved')",(uid, caption, url, type,))
    conn.commit()