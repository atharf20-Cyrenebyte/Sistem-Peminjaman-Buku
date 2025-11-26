from flask import Blueprint, request, jsonify
from models.models import db, Member


members_bp = Blueprint('members', __name__, url_prefix='/members')


@members_bp.route('', methods=['GET'])
def get_members():
    members = Member.query.all()
    data = [{"id": m.id, "name": m.name, "address": m.address, "phone": m.phone} for m in members]
    return jsonify(data)


@members_bp.route('/<int:id>', methods=['GET'])
def get_member(id):
    m = Member.query.get_or_404(id)
    return jsonify({"id": m.id, "name": m.name, "address": m.address, "phone": m.phone})


@members_bp.route('', methods=['POST'])
def create_member():
    payload = request.get_json() or {}
    name = payload.get('name')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    member = Member(name=name, address=payload.get('address'), phone=payload.get('phone'))
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'member created', 'id': member.id}), 201


@members_bp.route('/<int:id>', methods=['PUT'])
def update_member(id):
    m = Member.query.get_or_404(id)
    payload = request.get_json() or {}
    m.name = payload.get('name', m.name)
    m.address = payload.get('address', m.address)
    m.phone = payload.get('phone', m.phone)
    db.session.commit()
    return jsonify({'message': 'member updated'})


@members_bp.route('/<int:id>', methods=['DELETE'])
def delete_member(id):
    m = Member.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': 'member deleted'})