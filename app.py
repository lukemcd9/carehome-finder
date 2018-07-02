from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_login import LoginManager
from passlib.hash import sha512_crypt

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

photos = UploadSet('photos', IMAGES)

from views import *
from models import *

configure_uploads(app, photos)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def create_user(username, password):
    user = User(username=username, password=sha512_crypt.encrypt(password))

    already_registered = User.query.filter_by(username=username).first() is not None

    if not already_registered:
        db.session.add(user)
        db.session.commit()
        print(username, 'successfully registered.')
    else:
        print(username, 'already registered.')

if __name__ == '__main__':
    app.run()

# 20 hours