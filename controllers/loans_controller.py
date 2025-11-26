from models.models import db, Loan, Book, Member
from datetime import date

class LoanController:

    @staticmethod
    def get_all():
        return Loan.query.all()

    @staticmethod
    def get_by_id(id):
        return Loan.query.get(id)

    @staticmethod
    def create(data):
        member = Member.query.get(data['member_id'])
        book = Book.query.get(data['book_id'])

        if not member:
            return None, 'Member not found'
        if not book:
            return None, 'Book not found'
        if book.stock <= 0:
            return None, 'Book is out of stock'

        loan = Loan(
            member_id=data['member_id'],
            book_id=data['book_id'],
            loan_date=date.today(),
            status='borrowed'
        )
        book.stock -= 1
        db.session.add(loan)
        db.session.commit()
        return loan, None

    @staticmethod
    def return_loan(loan):
        if loan.status == 'returned':
            return 'Loan already returned'

        book = Book.query.get(loan.book_id)
        loan.return_date = date.today()
        loan.status = 'returned'
        book.stock += 1
        db.session.commit()
        return None

    @staticmethod
    def delete(loan):
        db.session.delete(loan)
        db.session.commit()