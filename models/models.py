from flask_sqlalchemy import SQLAlchemy
from datetime import date


db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    year = db.Column(db.Integer)
    stock = db.Column(db.Integer, nullable=False, default=0)


class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(50))


class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum('borrowed','returned', name='status_enum'), nullable=False, default='borrowed')


    member = db.relationship('Member', backref=db.backref('loans', lazy=True))
    book = db.relationship('Book', backref=db.backref('loans', lazy=True))