from utils.db import db
import string
import random

def get_db():
    return db

def generate_random(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("username", db.String(100))
    email = db.Column("email", db.String(100))
    phno = db.Column("phno", db.String(100))
    passwd = db.Column("passwd", db.String(256))
    data = db.relationship('Data', backref='user')

    def __init__(self, name, email, phno, passwd):
        self.name = name
        self.email = email
        self.phno = phno
        self.passwd = passwd

class Data(db.Model):
    _did = db.Column("did", db.Integer, primary_key=True)
    img = db.Column("img", db.String(100))
    title = db.Column("title", db.String(100))
    content = db.Column("content", db.String(250))
    time = db.Column("time", db.String(100))
    address = db.Column("address", db.String(100))
    city = db.Column("city", db.String(100))
    type_ = db.Column("type_", db.String(100))
    like = db.Column("likes", db.BigInteger)
    uid = db.Column("uid", db.String(100), db.ForeignKey('user.id'))

    def __init__(self, img, title, content, time, uid, city, address, type_):
        self.img = img
        self.title = title
        self.content = content
        self.time = time
        self.uid = uid
        self.city = city
        self.address = address
        self.type_ = type_
        self.like = 0