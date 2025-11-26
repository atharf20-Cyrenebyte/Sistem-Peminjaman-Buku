from flask import Blueprint, request, jsonify
from datetime import date
from models.models import db, Book, Member, Loan


loans_bp = Blueprint('loans', __name__)

# ===============================
# GET ALL LOANS
# ===============================
@loans_bp.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    result = []

    for loan in loans:
        result.append({
            'id': loan.id,
            'member_id': loan.member_id,
            'book_id': loan.book_id,
            'loan_date': str(loan.loan_date),
            'return_date': str(loan.return_date) if loan.return_date else None,
            'status': loan.status
        })

    return jsonify(result), 200


# ===============================
# GET LOAN DETAIL BY ID
# ===============================
@loans_bp.route('/loans/<int:id>', methods=['GET'])
def get_loan(id):
    loan = Loan.query.get(id)

    if not loan:
        return jsonify({"error": "Loan not found"}), 404

    data = {
        'id': loan.id,
        'member_id': loan.member_id,
        'book_id': loan.book_id,
        'loan_date': str(loan.loan_date),
        'return_date': str(loan.return_date) if loan.return_date else None,
        'status': loan.status
    }

    return jsonify(data), 200


# ===============================
# GET LOANS BY MEMBER
# ===============================
@loans_bp.route('/members/<int:id>/loans', methods=['GET'])
def get_member_loans(id):
    loans = Loan.query.filter_by(member_id=id).all()
    result = []

    for loan in loans:
        result.append({
            'id': loan.id,
            'book_id': loan.book_id,
            'loan_date': str(loan.loan_date),
            'return_date': str(loan.return_date) if loan.return_date else None,
            'status': loan.status
        })

    return jsonify(result), 200


# ===============================
# CREATE NEW LOAN (BORROW BOOK)
# ===============================
@loans_bp.route('/loans', methods=['POST'])
def create_loan():
    data = request.get_json()
    member_id = data.get('member_id')
    book_id = data.get('book_id')

    if not member_id or not book_id:
        return jsonify({"error": "member_id and book_id are required"}), 400

    member = Member.query.get(member_id)
    book = Book.query.get(book_id)

    if not member:
        return jsonify({"error": "Member not found"}), 404

    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Business logic: check stock
    if book.stock <= 0:
        return jsonify({'error': 'Book is out of stock'}), 400

    # Reduce stock
    book.stock -= 1

    new_loan = Loan(
        member_id=member_id,
        book_id=book_id,
        loan_date=date.today(),
        status="borrowed"
    )

    db.session.add(new_loan)
    db.session.commit()

    return jsonify({"message": "Loan created successfully"}), 201


# ===============================
# RETURN BOOK
# ===============================
@loans_bp.route('/loans/<int:id>/return', methods=['PUT'])
def return_loan(id):
    loan = Loan.query.get(id)

    if not loan:
        return jsonify({"error": "Loan not found"}), 404

    if loan.status == "returned":
        return jsonify({"error": "Loan already returned"}), 400

    book = Book.query.get(loan.book_id)

    # Business logic: increase stock
    book.stock += 1

    loan.status = "returned"
    loan.return_date = date.today()

    db.session.commit()

    return jsonify({"message": "Book returned successfully"}), 200


# ===============================
# OPTIONAL – DELETE LOAN
# ===============================
@loans_bp.route('/loans/<int:id>', methods=['DELETE'])
def delete_loan(id):
    loan = Loan.query.get(id)

    if not loan:
        return jsonify({"error": "Loan not found"}), 404

    db.session.delete(loan)
    db.session.commit()

    return jsonify({"message": "Loan deleted successfully"}), 200
