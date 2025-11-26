from models.models import db, Member

class MemberController:
    @staticmethod
    def get_all():
        return Member.query.all()

    @staticmethod
    def get_by_id(id):
        return Member.query.get(id)

    @staticmethod
    def create(data):
        member = Member(**data)
        db.session.add(member)
        db.session.commit()
        return member

    @staticmethod
    def update(member, data):
        for key, value in data.items():
            setattr(member, key, value)
        db.session.commit()
        return member

    @staticmethod
    def delete(member):
        db.session.delete(member)
        db.session.commit()