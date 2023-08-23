from flask import Flask
from logging import DEBUG
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = b'S\x96\xb4\x0ea\xc0\x89R'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
 
login_manager = LoginManager(app)
app.logger.setLevel(DEBUG)

from flask_package import routes
    
