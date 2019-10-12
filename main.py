import sys
import os
import time

import flask
import requests

from wassengerBackend import blueprint as wassengerBackend_blueprint
from dialogflowBackend import blueprint as dialogflowBackend_blueprint

import bd

import mysql.connector

mydb = mysql.connector.connect(
  host="35.199.79.147",
  user="root",
  passwd="Zho9AKzqoGwr",
  database="goethe"
)

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")

for x in mydb:
  print(x)


print(mydb)

app = flask.Flask(__name__)

app.secret_key = 'secret'

app.register_blueprint(wassengerBackend_blueprint)
app.register_blueprint(dialogflowBackend_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Zho9AKzqoGwr@35.199.79.147/goethe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bd.db = bd.SQLAlchemy(app)

@app.route('/')
def index():
    context = {
        'title':'Hacka | Olivetti'
    }
    return (context)

if __name__ == "__main__":
    root_module = os.path.abspath(os.path.curdir)
    sys.path.append(root_module)
    app.run(host='0.0.0.0')