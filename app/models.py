from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(64), index=True, unique=True)
    email = db.Column(db.Unicode(320), index=True, unique=True)
    password_hash = db.Column(db.Unicode(128))
    books = db.relationship('Book', back_populates='owners', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(200))

    def __repr__(self):
        return '<Author {}>'.format(self.name)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(120))
    # When referenceing in ForeignKey must use lower-case?
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    purchase_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    owners = db.relationship('User', back_populates='books', lazy='dynamic')

    def __repr__(self):
        return '<Book {}>'.format(self.title)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    note = db.Column(db.UnicodeText)

    def __repr__(self):
        return '<Note {}>'.format(note[0:10])