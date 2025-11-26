from flask import Blueprint, request, jsonify
from models.models import db, Book


books_bp = Blueprint('books', __name__, url_prefix='/books')


@books_bp.route('', methods=['GET'])
def get_books():
    books = Book.query.all()
    data = [
    {"id": b.id, "title": b.title, "author": b.author, "publisher": b.publisher, "year": b.year, "stock": b.stock}
    for b in books
    ]
    return jsonify(data)


@books_bp.route('/<int:id>', methods=['GET'])
def get_book(id):
    b = Book.query.get_or_404(id)
    return jsonify({"id": b.id, "title": b.title, "author": b.author, "publisher": b.publisher, "year": b.year, "stock": b.stock})


@books_bp.route('', methods=['POST'])
def create_book():
    payload = request.get_json() or {}
    title = payload.get('title')
    stock = payload.get('stock', 0)
    if title is None:
        return jsonify({'error': 'title is required'}), 400
    if stock < 0:
        return jsonify({'error': 'stock cannot be negative'}), 400


    book = Book(title=title, author=payload.get('author'), publisher=payload.get('publisher'), year=payload.get('year'), stock=stock)
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'book created', 'id': book.id}), 201


@books_bp.route('/<int:id>', methods=['PUT'])
def update_book(id):
    b = Book.query.get_or_404(id)
    payload = request.get_json() or {}
    if 'stock' in payload and payload['stock'] < 0:
        return jsonify({'error': 'stock cannot be negative'}), 400
    b.title = payload.get('title', b.title)
    b.author = payload.get('author', b.author)
    b.publisher = payload.get('publisher', b.publisher)
    b.year = payload.get('year', b.year)
    if 'stock' in payload:
        b.stock = payload['stock']
        db.session.commit()
        return jsonify({'message': 'book updated'})


@books_bp.route('/<int:id>', methods=['DELETE'])
def delete_book(id):
    b = Book.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    return jsonify({'message': 'book deleted'})