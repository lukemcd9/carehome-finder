from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from views import *
from models import *

if __name__ == '__main__':
    app.run()

# 20 hours