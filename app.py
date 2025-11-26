from flask import Flask, jsonify
from config.config import Config
from models.models import db


from routes.books import books_bp
from routes.members import members_bp
from routes.loans import loans_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)


    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(loans_bp)


    @app.route('/')
    def hello():
        return jsonify({'message': 'Perpustakaan API running'})

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all() # untuk development; di production gunakan migration
    app.run(debug=True)