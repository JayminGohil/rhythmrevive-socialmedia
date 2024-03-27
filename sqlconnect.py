import mysql.connector
from rhythmrevive import app

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rhythmdb',
    'auth_plugin': ''
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()