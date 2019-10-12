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


def insert_user(data, table):
    result = hashlib.md5(str(datetime.now()).encode())
    sql = "INSERT INTO " + table + " (phone, name, conversationid) VALUES (%s, %s, %s)"
    val = (data.phone, "default - name", str(result.hexdigest()))
    mycursor.execute(sql, val)
    mydb.commit()

def find_user(query, table, key, value):
    sql = "SELECT * FROM " + table + " WHERE " + key + " ='"+ value +"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        query.id = x[0]
        query.name = x[2]
        query.phone = x[1]
        query.conversationid = x[3]
    return query

def select_all_users(table):
    mycursor.execute("SELECT * FROM " + table)
    myresult = mycursor.fetchall()
    usersData = []
    index = 0
    for x in myresult:
        context = {
            'id':int(x[0]),
            'phone':str(x[1]),
            'name':str(x[2]),
            'conversationid':str(x[3])
        }
        usersData.insert(index, context)
        index = index + 1
    return(usersData)



#def update_user(userPhone, new_Name):
    #upd = db.update(users).where(users.phone == userPhone).values(name=new_Name)
    #db.session.execute(upd)
    #db.session.commit()
    #print("USUÁRIO ATUALIZADO")

#def reset_users():
    #upd = db.update(users).values(name="")
    #db.session.execute(upd)
    #db.session.commit()