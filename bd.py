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


def insert_user(data, table, key, value):
    result = hashlib.md5(str(datetime.now()).encode())
    sql = "INSERT INTO " + table + " (phone, name, conversationid, newsid) VALUES (%s, %s, %s, %s)"
    val = (data.phone, "default - name", str(result.hexdigest()), 0)
    mycursor.execute(sql, val)
    mydb.commit()
    data = find_user(data, table, key, value)
    return data

def find_user(data, table, key, value):
    sql = "SELECT * FROM " + table + " WHERE " + key + " ='"+ value +"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        data.id = x[0]
        data.name = x[2]
        data.phone = x[1]
        data.conversationid = x[3]
    return data

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


def insert_news(data, table, key, value):
    sql = "INSERT INTO " + table + " (url, userid) VALUES (%s, %s)"
    val = (data.url, data.userid)
    #print(data.url)
    mycursor.execute(sql, val)
    mydb.commit()
    data = find_news(data, table, key, value)
    return data

def find_news(data, table, key, value):
    sql = "SELECT * FROM " + table + " WHERE " + key + " ='"+ value +"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        data.id = x[0]
        data.url = x[1]
        data.userid = x[2]
    return data

def find_votes(table, key, value):
    sql = "SELECT * FROM " + table + " WHERE " + key + " ='"+ str(value) +"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    votes = [0,0,0]
    for x in myresult:
        if(x[3] == 0): votes[0] = votes[0] + 1
        if(x[3] == 1): votes[1] = votes[1] + 1
        if(x[3] == 2): votes[2] = votes[2] + 1
    return votes

#def look_for_user_votes(data, table, key, value){
#    sql = "SELECT * FROM " + table
#    mycursor.execute(sql)
#    myresult = mycursor.fetchall()
    #for x in myresult:

#}

def update_user(table, keytoupdate, valuetoupdate, key, value):
    sql = "UPDATE " + table + " SET " + keytoupdate + " = '" + valuetoupdate + "' WHERE " + key + " = '" + value + "'"
    mycursor.execute(sql)
    mydb.commit()

    print(mycursor.rowcount, "record(s) affected")
#def update_user(userPhone, new_Name):
    #upd = db.update(users).where(users.phone == userPhone).values(name=new_Name)
    #db.session.execute(upd)
    #db.session.commit()
    #print("USUÁRIO ATUALIZADO")

#def reset_users():
    #upd = db.update(users).values(name="")
    #db.session.execute(upd)
    #db.session.commit()