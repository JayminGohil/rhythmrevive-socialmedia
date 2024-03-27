from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
from werkzeug.security import generate_password_hash, check_password_hash
import time

@app.route('/adminPanel/manageAdmin',methods=['GET', 'POST'])
def manageAdmin():
    if 'admin' in session:
        adminName = session.get('admin')
        if request.method == 'POST':
            newadminusername = request.form['newadminusername']
            newadminpassword = request.form['newadminpassword']
            if checkAdminUsername(newadminpassword):
                msg = "Admin Username Already Exists"
                return render_template('adminManage.html',msg=msg)
            encPass = generate_password_hash(newadminpassword, method='scrypt')
            insertAdmin(newadminusername,encPass)
            msg = "New Admin Account Created!"
            return render_template('adminManage.html',msg=msg,adminName=adminName)
        return render_template('adminManage.html',adminName=adminName)
    else:
        return redirect(url_for('adminLogin'))
    

def insertAdmin(username,password):
    cursor.execute("INSERT INTO admins(admin_username,admin_password,created_at) VALUES(%s,%s,NOW())",(username,password,))
    conn.commit()

def checkAdminUsername(username):
    cursor.execute("SELECT * FROM admins WHERE admin_username=%s",(username,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False


@app.route('/getAdmins', methods=['GET', 'POST'])
def getAdmins():
    cursor.execute("SELECT admin_id, admin_username, created_at FROM admins")
    result = cursor.fetchall()
    admins_data = [{'admin_id': row[0], 'admin_username': row[1], 'created_at': row[2]} for row in result]
    return jsonify({'admins': admins_data})


@app.route('/deleteAdmin', methods=['POST'])
def deleteAdmin():
    try:
        admin_id = request.form.get('id')
        cursor.execute("DELETE FROM admins WHERE admin_id = %s", (admin_id,))
        conn.commit()
        return 'Admin deleted successfully', 200
    except Exception as e:
        return str(e), 500