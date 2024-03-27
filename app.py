from flask import render_template,session,redirect,url_for
from rhythmrevive import app
from flask_socketio import SocketIO,send,emit
from register import app as register_app
from login import app as login_app
from verify import app as verify_app
from index import app as index_app
from createPost import app as createPost_app
from userProfile import app as userProfile_app
from editProfile import app as editProfile_app
from forgot import app as forgot_app
from follow import app as follow_app
from searchUser import app as searchUser_app
from fetchPosts import app as fetchPosts_app
from likeNdCmnt import app as likeNdCmnt_app
from lessonsAndSheet import app as lessonsAndSheet_app
from messages import app as messages_app
from messageUser import app as messageUser_app
from forums import app as forums_app
from saveMsg import addMessageToDb
from admin import adminIndex,adminLogin,adminAnalytics,adminManage,adminBadges,adminModeration,adminPosts
import json

socketio = SocketIO(app,cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    if data!='':
        print(data)
        datajson = json.loads(data)
        message = datajson["message"]
        sender_id = datajson["sender_id"]
        receiver_id = datajson["receiver_id"]
        addMessageToDb(message,sender_id,receiver_id)
        if data != "User Connected!":
            send(data, broadcast=True)
    else:
        print('no data')

def custom_enumerate(iterable):
    return zip(range(len(iterable)), iterable)
app.jinja_env.filters['custom_enumerate'] = custom_enumerate

if __name__ == '__main__':
    socketio.run(app, debug=True)