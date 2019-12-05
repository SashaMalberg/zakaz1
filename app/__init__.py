from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from config import Config
import psycopg2
import os

app = Flask(__name__)
app.config.from_object(Config)
POSTGRES_URL = "127.0.0.1:5432"
POSTGRES_USER = "postgres"
POSTGRES_PW = "root"
POSTGRES_DB = "test"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                                   db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = "super_key"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
admin = Admin(app, template_mode='bootstrap3')

from app import routes, models
