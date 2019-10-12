from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(100))
    name = db.Column(db.String(100))
    def __init__(self, phone, name):
        self.phone = phone
        self.name = name

def insert_user(data):
    print("test")
    usr = users(data.phone, data.name)
    db.session.add(usr)
    db.session.commit()

def select_all_users():
    data_users = users.query.all()
    usersData = []
    for num, item in enumerate(data_users, start=0):
        context = {
            'phone':str(item.phone),
            'name':str(item.name)
        }
        usersData.insert(num, context)
    return(usersData)

def find_user(query_phone):
    user = users.query.filter_by(phone=query_phone).first()
    if(user != None): return user
    else: return None

def update_user(userPhone, new_Name):
    upd = db.update(users).where(users.phone == userPhone).values(name=new_Name)
    db.session.execute(upd)
    db.session.commit()
    print("USUÁRIO ATUALIZADO")

def reset_users():
    upd = db.update(users).values(name="")
    db.session.execute(upd)
    db.session.commit()