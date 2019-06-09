import datetime
from app import db
from werkzeug.security import generate_password_hash
        
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    trn = db.Column(db.String(9), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(255), nullable=True, unique=True)
    address = db.Column(db.String(255), nullable=False)
    joined_on = db.Column(db.Date, nullable=False, default=datetime.datetime.now())
    
    posts = db.relationship('Post', backref='User', passive_deletes=True, lazy=True)
    
    def __init__(self, trn, username, password, firstname, lastname, email, 
                phone, address):

                self.trn = trn 
                self.username = username
                self.password = generate_password_hash(password, method='pbkdf2:sha256')
                self.firstname = firstname
                self.lastname = lastname
                self.email = email
                self.phone = phone
                self.address = address


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_trn = db.Column(db.Integer, db.ForeignKey('users.trn', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.Date, default=datetime.datetime.now(), nullable=False)
    
    def __init__(self, user_trn, title, content):
        self.user_trn = user_trn
        self.title = title
        self.content = content
        
