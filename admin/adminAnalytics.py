from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import random
from sqlconnect import conn,cursor
from rhythmrevive import app
import time

@app.route('/adminPanel/analytics')
def adminAnalytics():
    if 'admin' in session:
        adminName = session.get('admin')
        usersData = usersAnalytics()
        return render_template('adminAnalytics.html',usersData=usersData,adminName=adminName)
    else:
        return redirect(url_for('adminLogin'))



def usersAnalytics():
    cursor.execute("""SELECT date_range.date AS creation_date, 
       COUNT(u.user_creation_timestamp) AS users_created
FROM (
    SELECT CURDATE() - INTERVAL (t4.i*10000 + t3.i*1000 + t2.i*100 + t1.i*10 + t0.i) DAY AS date
    FROM 
        (SELECT 0 AS i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS t0,
        (SELECT 0 AS i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS t1,
        (SELECT 0 AS i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS t2,
        (SELECT 0 AS i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS t3,
        (SELECT 0 AS i UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS t4
    WHERE (t4.i*10000 + t3.i*1000 + t2.i*100 + t1.i*10 + t0.i) <= 6
) AS date_range
LEFT JOIN rhythmdb.users u
    ON DATE(u.user_creation_timestamp) = date_range.date
GROUP BY date_range.date
ORDER BY date_range.date;
    """)
    result = cursor.fetchall()
    return result