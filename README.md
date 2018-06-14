Install MySQL and Python3
```shell
pip install virtualenv
```
In the project folder
```shell
virtualenv env
source env/Scripts/activate
```
Install Requirements
```shell
pip install -r requirements.txt
```
Make config.py
```python
DEBUG = True
SECRET_KEY = 'super-secret'
SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/database?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True
```
Setup database
```shell
python

    from app import db
    db.create_all()
    quit()
```
Run the development server
```shell
python app.py
```