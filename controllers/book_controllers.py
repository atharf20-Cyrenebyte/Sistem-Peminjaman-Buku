from models.models import db, Book

class BookController:
    @staticmethod
    def get_all():
        return Book.query.all()

    @staticmethod
    def get_by_id(id):
        return Book.query.get(id)

    @staticmethod
    def create(data):
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def update(book, data):
        for key, value in data.items():
            setattr(book, key, value)
        db.session.commit()
        return book

    @staticmethod
    def delete(book):
        db.session.delete(book)
        db.session.commit()