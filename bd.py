from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime

import mysql.connector

mydb = mysql.connector.connect(
  host="35.199.79.147",
  user="root",
  passwd="Zho9AKzqoGwr",
  database="goethe"
)

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")


sql = "SELECT * FROM users WHERE phone ='"+ "123567" +"'"

mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
  print(x)



db = SQLAlchemy()

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(100))
    name = db.Column(db.String(100))
    conversationid = db.Column(db.String(500))
    def __init__(self, phone, name, conversationid):
        self.phone = phone
        self.name = name
        self.conversationid = conversationid

def insert_user(data):
    result = hashlib.md5(str(datetime.now()).encode())
    sql = "INSERT INTO users (phone, name, conversationid) VALUES (%s, %s, %s)"
    val = (data.phone, "default - name", str(result.hexdigest()))
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

    #return find_user(data)

def find_user(query):
    result = users.query.filter_by(phone=query.phone).first()
    if(result != None): 
        print("found")
        query.name = result.name
        query.phone = result.phone
        query.conversationid = result.conversationid
    return query

def select_all_users():
    data_users = users.query.all()
    usersData = []
    for num, item in enumerate(data_users, start=0):
        context = {
            'phone':str(item.phone),
            'name':str(item.name),
            'conversationid':str(item.conversationid)
        }
        usersData.insert(num, context)
    return(usersData)



def update_user(userPhone, new_Name):
    upd = db.update(users).where(users.phone == userPhone).values(name=new_Name)
    db.session.execute(upd)
    db.session.commit()
    print("USUÁRIO ATUALIZADO")

def reset_users():
    upd = db.update(users).values(name="")
    db.session.execute(upd)
    db.session.commit()