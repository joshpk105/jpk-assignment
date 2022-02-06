from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(64), index=True, unique=True)
    email = db.Column(db.Unicode(320), index=True, unique=True)
    password_hash = db.Column(db.Unicode(128))
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Shouldn't this be done on the users computer in javascript?
    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)
    
    # This function should be taking a hash?
    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(200))

    def __repr__(self):
        return '<Author {}>'.format(self.name)

class Authorship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __repr__(self):
        return '<Authorship {}->{}>'.format(self.author_id, self.book_id)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(120))

    def __repr__(self):
        return '<Book {}>'.format(self.title)

class Ownership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __repr__(self):
        return '<Ownership {}>'.format(purchase_datetime)