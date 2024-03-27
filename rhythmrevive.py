from flask import Flask,session
from flask_mail import Mail
from colorama import Fore, Style

def rhythmrevive():
    app = Flask(__name__)
    app.secret_key = 'RhythmreviveTyIMScIT'
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'example@gmail.com' # Your Email Here
    app.config['MAIL_PASSWORD'] = 'abcdefghijklmnop' # Your Password Here (16 Digits Without Any Space or Dash)
    app.config['MAIL_DEFAULT_SENDER'] = 'example@gmail.com' # Your Email Here
   
    mail = Mail(app)
    return app, mail
app, mail = rhythmrevive()
