# -*- coding: utf-8 -*-
import json
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#mail = Mail(app)
with open('./libailul/libaile/datas/secret.json', 'r') as secret_file:
    secret = json.load(secret_file)
    SECRET_KEY = secret['secret_key']
    MAIL_USERNAME = secret['mail_username']
    MAIL_PASSWORD = secret['mail_password']

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USE_SSL'] = True

#mail = Mail(app)

from libaile import routes
