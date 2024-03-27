from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from sqlconnect import conn,cursor
from rhythmrevive import app

def addMessageToDb(message,sender_id,receiver_id):
    cursor.execute("INSERT INTO messages(sender_id, receiver_id,content, timestamp) VALUES (%s, %s,%s,NOW())",(sender_id, receiver_id, message,))
    conn.commit()