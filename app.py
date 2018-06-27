from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from views import *
from models import *

photos = UploadSet('photos', IMAGES)

configure_uploads(app, photos)

if __name__ == '__main__':
    app.run()

# 20 hours